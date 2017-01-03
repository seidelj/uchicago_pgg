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
This is 4-period public goods game with 16 players.  Assignment to the group is predermined

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

        # Displays order in the logs at creation of session
        if self.round_number == Constants.starting_rounds[0]:
            order = Constants.mpcrOrders[self.session.config['mpcrOrder'] - 1]
            for k, v in order.items():
                if v == "vr": self.session.vars['varied_round'] = k
            print("Order {}: {}".format(self.session.config['mpcrOrder'], order))

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
            self.set_groups(list_of_lists)


        # set efficiency rate and noisy signals
        #for group in self.get_groups():
        #    if group.efficiency_rate == None:
        #        group.set_efficiency_rate()
        #        group.set_varying_efficiency_rate()
        self.set_efficiency_rate()
        self.set_varying_efficiency_rate()
        for p in self.get_players():
            p.set_signal_value()
            p.set_group_id()

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

#def determine_round(player):
#    x = 0
#    for r in Constants.starting_rounds:
#        if player.subsession.round_number in range(r, r+Constants.rounds_per_game):
#            game_number = x
#            break
#        else:
#            x += 1
#    return x

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    individual_share = models.DecimalField(max_digits=12, decimal_places=2)

    efficiency_rate = models.DecimalField(max_digits=12, decimal_places=2)

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
            p.potential_payoff = (Constants.endowment - p.contribution) + self.individual_share
            if x <= self.subsession.round_number <= x + 7:
                p.payoff = p.potential_payoff * self.session.real_world_currency_per_point
                p.points = p.potential_payoff
            else:
                p.points = 0
                p.payoff = 0

    def set_game_payoffs(self):
        for p in self.get_players():
            p.set_session_payoffs()

class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    treatment = models.IntegerField()

    contribution = models.DecimalField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        max_digits=12, decimal_places=2,
    )

    signal = models.DecimalField(max_digits=12, decimal_places=2)
    potential_payoff = models.DecimalField(max_digits=12, decimal_places=2)
    points = models.DecimalField(max_digits=12, decimal_places=2)

    sub_group_id = models.CharField()

    def set_group_id(self):
        players = self.subsession.get_players()
        if len(players) == 16:
            for item in self.in_all_rounds():
                if item.subsession.round_number in Constants.starting_rounds:
                    players = item.subsession.get_players()
                    rn = item.subsession.round_number
                    newPlayerOrder = reorder_group(players, GROUP_DICT[rn])
                    num_groups = int(len(players) / Constants.players_per_group)
                    list_of_lists = []
                    start_index = 0
                    for g_num in range(num_groups):
                        next_group = newPlayerOrder[start_index:start_index+Constants.players_per_group]
                        start_index += Constants.players_per_group
                        list_of_lists.append(next_group)
                    for l in list_of_lists:
                        if item in l:
                            indx = list_of_lists.index(l)
                    item.sub_group_id = "{}{}".format(rn, indx)
                else:
                    item.sub_group_id = item.in_previous_rounds()[-1].sub_group_id

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
            payoffs.append(p.potential_payoff)
        return sum(payoffs)

    def set_session_payoffs(self):
        self.participant.vars['pg_points'] = sum([p.points for p in self.in_all_rounds()])
        self.participant.vars['pg_payoff'] = sum([p.payoff for p in self.in_all_rounds()])
