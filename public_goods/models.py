# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random, time
from decimal import *
# </standard imports>

doc = """
This is a 4 games of 8 rounds public goods game with 16 players.

Note on points and payoff:  The subjects are given tokens which are converted to US dollars at the end of the session.  1 token = $.05

Assignment to the group is predetermined.  Row is group for each game.  Add 1 to each number, e.g. player 1 == 0.

Game 1:
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 13, 14, 15,

Game 2:
    0, 4, 8, 12,
    1, 5, 9, 13,
    2, 6, 10, 14,
    3, 7, 11, 15,

Game 3:
    0, 5, 10, 15,
    1, 6, 11, 12,
    2, 7, 8, 13,
    3, 4, 9, 14,

Game 4:
    0, 7, 9, 13,
    1, 4, 8, 10,
    2, 5, 11, 12,
    3, 6, 14, 15,


Treatment Dummies:

    Treatment 1: Public Goods Baseline
    Treatment 2: Public Goods Private Signal
    Treatment 3: Public Goods Public Signal


Order Dummies (mpcr_order):

    Order 1: .25, .55, .95, varied
    Order 2: .95, .55, .25, varied
    Order 3: .55, .25, .95, varied
    Order 4: .25, .95, .55, varied

"""


source_code = "https://github.com/seidelj/uchicago_pgg"


bibliography = ()


links = {
    "Wikipedia": {
        "Public Goods Game": "https://en.wikipedia.org/wiki/Public_goods_game"
    }
}


keywords = ("Public Goods",)

def create_efficiency_list():
    numlist = []
    x = 0
    while x < 8:
        number = random.choice(Constants.efficiency_factors)
        if numlist.count(number) < 2:
            numlist.append(number)
            x += 1
    return numlist

class Constants:
    name_in_url = 'public_goods'
    players_per_group = 4
    num_rounds = 32
    rounds_per_game = 8
    starting_rounds = [
        1, rounds_per_game+1,
    rounds_per_game*2+1, rounds_per_game*3+1
    ]

    #"""Amount allocated to each player"""
    template_endowment = 10
    endowment = c(template_endowment)
    efficiency_factor = 2
    base_points = c(10)
    efficiency_floats = [
    .05, .15, .25, .35,
    .45, .55, .65, .75,
    .85, .95, 1.05,
    1.15, 1.25,
    ]
    getcontext().prec = 28
    efficiency_factors =[Decimal(x).quantize(Decimal('.01')) for x in efficiency_floats]

    fMPCRS = [.25, .55, .95]
    MPCRS = [Decimal(x).quantize(Decimal('.01')) for x in fMPCRS]
    question_correct = c(92)

    # order of MPCR values 3 = Varied round
    orders = [
    [0, 1, 2, 3],
    [2, 1, 0, 3],
    [1, 0, 2, 3],
    [0, 2, 1, 3],
    ]

    mpcrOrders = []
    for o in orders:
        od = {}
        for x in range(4):
            mpcr = MPCRS[o[x]] if o[x] != 3 else "vr"
            od[starting_rounds[x]] = mpcr
        mpcrOrders.append(od)

def reorder_group(players, order):
    #SORT PLAYERS TO MAKE SURE ORDERING IS DONE RIGHT!
    players.sort(key=lambda x: x.participant.id, reverse=False)
    newlist = []
    for item in order:
        newlist.append(players[item])
    return newlist

GROUP_DICT = {
    1: [
        0, 1, 2, 3,
        4, 5, 6, 7,
        8, 9, 10, 11,
        12, 13, 14, 15,
    ],
    9: [
        0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15,
    ],
    17: [
        0, 5, 10, 15,
        1, 6, 11, 12,
        2, 7, 8, 13,
        3, 4, 9, 14,
    ],
    25: [
        0, 7, 9, 13,
        1, 4, 8, 10,
        2, 5, 11, 12,
        3, 6, 14, 15,
    ],
}

class Subsession(otree.models.BaseSubsession):

    paying_game = models.CharField(
        doc="0 if the game is a hypothetical round, 1 otherwise"
    )
    game_number = models.CharField(
        doc="Each player plays 4 games, each against different player.  This variable indicates which is being played."
    )
    game_round = models.CharField(
        doc="Each game is 8 rounds, this variables tells you which.")
    mpcr_order = models.CharField(
        doc="Dummy variable for the order of MPRC's seen across the 4 games a participant plays.  See above"
    )
    varied_mpcr_game = models.CharField(
        doc="In one of the 4 games plays, the MPCR is varied each round.  1 if that is happening in the observed round, 0 otherwise"
    )
    treatment = models.CharField(
        doc="Dummy variable for the treatment of the observed session. See above"
    )
    signalVariance = models.CharField(
        doc="Think of this as the size of the signal that a participant observes.  0:Exact value; 1:Thin signal; 2:Thick signal;"
    )

    app_label = models.CharField(default="public_goods", doc="the application that produced the observed row")

    def get_all_rounds(self):
        qs = type(self).objects.filter(session_id=self.session_id).order_by('round_number')
        return list(qs)

    def before_session_starts(self):
        # Get treatment from SessionStore
        for p in self.get_players():
            p.treatment = self.session.config['treatment']

        # Determine paying game
        if self.round_number == Constants.starting_rounds[0]:
            print("Assigning paying round")
            paying_round = random.choice(Constants.starting_rounds)
            self.session.vars['paying_round'] = paying_round

        #Set a bunch of variables for data export
        #Determine which game, round and whether the stakes are real.
        x = 1
        for r in Constants.starting_rounds:
            if self.round_number in range(r, r+Constants.rounds_per_game):
                game_number = x
                break
            else:
                x += 1
        game_round = (self.round_number - Constants.starting_rounds[x-1]) + 1

        if self.round_number in range(self.session.vars['paying_round'], self.session.vars['paying_round']+Constants.rounds_per_game):
            self.paying_game = 1
        else:
            self.paying_game = 0
        self.game_number = game_number
        self.game_round = game_round
        self.mpcr_order = self.session.config['mpcrOrder']
        self.treatment = self.session.config['treatment']
        self.signalVariance = self.session.config['signalVariance']
        self.save()

        # Displays order in the logs at creation of session
        if self.round_number == Constants.starting_rounds[0]:
            order = Constants.mpcrOrders[self.session.config['mpcrOrder'] - 1]
            for k, v in order.items():
                if v == "vr": self.session.vars['varied_round'] = k
            print("Order {}: {}".format(self.session.config['mpcrOrder'], order))

        #Set varied mpcr round for data export
        if self.round_number in range(self.session.vars['varied_round'], self.session.vars['varied_round']+Constants.rounds_per_game):
            self.varied_mpcr_game = 1
        else:
            self.varied_mpcr_game = 0
        self.save()

        # Reorder teams in between games
        if self.round_number in Constants.starting_rounds:
            players = self.get_players()
            if len(players) == 16:
                newPlayerOrder = reorder_group(players, GROUP_DICT[self.round_number])
            else:
                newPlayerOrder = sorted(players, key=lambda *args: random.random())
            num_groups = int(len(players) / Constants.players_per_group)
            list_of_lists = []
            start_index = 0
            for g_num in range(num_groups):
                next_group = newPlayerOrder[start_index:start_index+Constants.players_per_group]
                start_index += Constants.players_per_group
                list_of_lists.append(next_group)
            self.set_group_matrix(list_of_lists)
        else:
            self.group_like_round(self.round_number-1)


        # set efficiency rate and noisy signals
        #for group in self.get_groups():
        #    if group.efficiency_rate == None:
        #        group.set_efficiency_rate()
        #        group.set_varying_efficiency_rate()
        self.set_efficiency_rate()
        self.set_varying_efficiency_rate()
        for p in self.get_players():
            p.set_signal_value()


    def set_efficiency_rate(self):
        order = Constants.mpcrOrders[self.session.config['mpcrOrder'] - 1]
        vr = self.session.vars['varied_round']
        if self.round_number not in range(vr, vr+Constants.rounds_per_game):
            if self.round_number in Constants.starting_rounds:
                newMpcr = order[self.round_number]
            else:
                newMpcr = self.in_previous_rounds()[-1].get_groups()[0].efficiency_rate
            for group in self.get_groups():
                group.efficiency_rate = newMpcr

    def set_varying_efficiency_rate(self):
        vr = self.session.vars['varied_round']
        pastMpcrs = []
        fixed_rounds = []
        for s in self.in_all_rounds():
            if s.round_number in Constants.starting_rounds:
                pastMpcrs = []
            else:
                pastMpcrs.append(s.get_groups()[0].efficiency_rate)
        newMpcr = False
        while not newMpcr:
            number = random.choice(Constants.efficiency_factors)
            if pastMpcrs.count(number) < 2:
                newMpcr = number
        if self.round_number in range(vr, vr+Constants.rounds_per_game):
            for group in self.get_groups():
                group.efficiency_rate = newMpcr

class Group(otree.models.BaseGroup):

    total_contribution = models.DecimalField(max_digits=12, decimal_places=2,
        doc="The aggregate of all member's of a given game's contributions"
    )
    individual_share = models.DecimalField(max_digits=12, decimal_places=2,
        doc="total_contribution divided by 4"
    )

    efficiency_rate = models.DecimalField(max_digits=12, decimal_places=2,
        doc="This is the group's true MPCR"
    )

    def set_efficiency_rate(self):
        #Used for singular MPRC throughout the game
        # Get the MPRCs for each game
        vr = self.session.vars["varied_round"]
        pastMpcrs = []
        fixed_rounds = []
        player = self.get_players()[0]
        for f in player.in_all_rounds():
            # only do this for starting rounds that are to reamin fixed
            if f.subsession.round_number not in range(vr, vr+Constants.rounds_per_game):
                if f.subsession.round_number in Constants.starting_rounds:
                    fixed_rounds.append(f.subsession.round_number)
                    pastMpcrs.append(f.group.efficiency_rate)

        # determine whether to select a new MPCR or use an old one
        if self.subsession.round_number not in range(vr, vr+Constants.rounds_per_game):
            if self.subsession.round_number in fixed_rounds:
                newMpcr = False
                while not newMpcr:
                    number = random.choice(Constants.MPCRS)
                    if pastMpcrs.count(number) < 1:
                        newMpcr = number
            else:
                player = self.get_players()[0]
                newMpcr = player.in_previous_rounds()[-1].group.efficiency_rate

        # Make sure that an MPCR is not getting set in the varied round
        if self.subsession.round_number not in range(vr, vr+Constants.rounds_per_game):
            self.efficiency_rate = newMpcr

    def set_varying_efficiency_rate(self):
        #Used for different efficiency rates throughout game
        vr = self.session.vars['varied_round']
        pastMpcrs = []
        player = self.get_players()[0]
        for f in player.in_all_rounds():
            if f.subsession.round_number in Constants.starting_rounds:
                pastMpcrs = []
            else:
                pastMpcrs.append(f.group.efficiency_rate)
        newMpcr = False
        while not newMpcr:
            number = random.choice(Constants.efficiency_factors)
            if pastMpcrs.count(number) < 2:
                newMpcr = number
        if self.subsession.round_number in range(vr, vr+Constants.rounds_per_game):
            self.efficiency_rate = newMpcr

    def set_payoffs(self):
        # add some logic here to add up contributions
        # from rounds 1-10, 11-20, 21-30
        x = self.session.vars['paying_round']
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * self.efficiency_rate
        for p in self.get_players():
            p.hypothetical_points = (Constants.endowment - p.contribution) + self.individual_share
            if x <= self.subsession.round_number <= x + 7:
                p.payoff = p.hypothetical_points * self.session.real_world_currency_per_point
                p.points = p.hypothetical_points
            else:
                p.points = 0
                p.payoff = 0

    def set_game_payoffs(self):
        for p in self.get_players():
            p.set_session_payoffs()


class Player(otree.models.BasePlayer):

    treatment = models.IntegerField(
        doc="The player's treatment; identical to subsession.treatment"
    )

    contribution = models.DecimalField(
        min=0, max=Constants.endowment,
        max_digits=12, decimal_places=2,
        doc="The amount the player contributed for the observed round",
    )

    signal = models.DecimalField(max_digits=12, decimal_places=2,
        doc="The signal observed by the player in given round",
    )
    hypothetical_points = models.DecimalField(max_digits=12, decimal_places=2,
        doc="The value of group contributions divided by 4 for a given round plus whatever remains from the player's endowment.  This varaible is required by the application when determining payouts because stakes are not always real"
    )
    points = models.DecimalField(max_digits=12, decimal_places=2,
        doc="The same as player.hypothetical_points except this only gets populated when stakes are real.  The variable is required by the application when determining payouts because stakes are not always real"
    )

    def set_signal_value(self):
        rn = self.subsession.round_number
        vr = self.session.vars['varied_round']
        signalVariance = self.session.config['signalVariance']
        if rn in Constants.starting_rounds or rn in range(vr, vr+Constants.rounds_per_game):
            mpcr = self.group.efficiency_rate
            choicesLeft = [mpcr - Decimal(x*.1) for x in range(1, signalVariance + 1)]
            choicesRight = [mpcr + Decimal(x*.1) for x in range(1, signalVariance + 1)]

            #chop off choices if at the tails
            if mpcr < Decimal(.06):
                choices = choicesRight + [mpcr]
            elif Decimal(.06) < mpcr < Decimal(.16) and signalVariance == 2:
                choices = choicesRight + [mpcr] + choicesLeft[:1]
            elif mpcr > Decimal(1.16):
                choices = choicesLeft + [mpcr]
            elif Decimal(1.06) < mpcr < Decimal(1.16) and signalVariance == 2:
                choices = choicesLeft + [mpcr] + choicesRight[:1]
            else:
                choices = [mpcr] + choicesLeft + choicesRight
            signal = random.choice(choices)
            self.signal = signal.quantize(Decimal('.01'))
        else:
            self.signal = self.in_previous_rounds()[-1].signal

    def get_signal_values(self):
        if self.session.config['signalVariance'] == 2:
            signalVariance = Decimal(.2)
        else:
            signalVariance = Decimal(.1)
        left = self.signal - signalVariance
        right = self.signal + signalVariance
        signals = dict(left=left.quantize(Decimal('.01')), right=right.quantize(Decimal('.01')))
        return signals

    def get_game_info(self):
        for p in self.in_all_rounds():
            if p.subsession.round_number in Constants.starting_rounds:
                info = []
            info.append(p)
        return info

    def get_round_period(self):
        x = 1
        for r in Constants.starting_rounds:
            if self.subsession.round_number in range(r, r+Constants.rounds_per_game):
                game_round = self.subsession.round_number - r
                break
            else:
                x += 1
        game_round += 1
        return [game_round, x]

    def get_game_payoffs(self):
        for p in self.in_all_rounds():
            if p.subsession.round_number in Constants.starting_rounds:
                payoffs = []
            payoffs.append(p.hypothetical_points)
        return sum(payoffs)

    def set_session_payoffs(self):
        self.participant.vars['pg_points'] = sum([p.points for p in self.in_all_rounds()])
        self.participant.vars['pg_payoff'] = sum([p.payoff for p in self.in_all_rounds()])
