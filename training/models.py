# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from public_goods.models import Constants as PgConstants
from decimal import Decimal

# </standard imports>

author = 'Joseph Seidel'

doc = """
Training module for public goods game.
"""



class Constants:
    name_in_url = 'practice'
    players_per_group = 4
    num_rounds = 4
    rounds_per_game = 4
    #efficiency_rate = 1.8

    # define more constants here
    template_endowment = PgConstants.template_endowment
    endowment = PgConstants.endowment
    efficiency_factors = PgConstants.efficiency_factors
    MPCRS = PgConstants.MPCRS

class Subsession(otree.models.BaseSubsession):

    def get_all_rounds(self):
        qs = type(self).objects.filter(session_id=self.session_id).order_by('round_number')
        return list(qs)

    def before_session_starts(self):
        # get treatment from SessionStore
        for p in self.get_players():
            p.treatment = self.session.config['treatment']
        # Determine paying round
        if self.round_number == 1:
            print("Assigning paying round")
            paying_round = 1
            self.session.vars['paying_round'] = paying_round

        # Scramble teams between games

        # set efficiency rate and noisy signals
        for group in self.get_groups():
            if group.efficiency_rate == None:
                group.set_efficiency_rate()

        for group in self.get_groups():
            if group.subsession.round_number == 1:
                for player in group.get_players():
                    mpcr = group.efficiency_rate
                    left = mpcr - Decimal(.1)
                    right = mpcr + Decimal(.1)
                    signal = random.choice([mpcr, right, left])
                    player.signal = signal.quantize(Decimal('.01'))

        for p in self.get_players():
            p.set_signal_value()

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    individual_share = models.DecimalField(max_digits=12, decimal_places=2)

    #    efficiency_rate = models.FloatField()
    efficiency_rate = models.DecimalField(max_digits=12, decimal_places=2)

    def old_set_efficiency_rate(self):
        if self.subsession.round_number == 1:
            newMpcr = round(random.choice(Constants.efficiency_factors),2)
        else:
            player = self.get_players()[0]
            for f in player.in_all_rounds():
                if f.subsession.round_number == 1:
                    newMpcr = f.group.efficiency_rate
        self.efficiency_rate = newMpcr

    def set_efficiency_rate(self):
        pastMpcrs = []
        player = self.get_players()[0]
        for f in player.in_all_rounds():
            pastMpcrs.append(f.group.efficiency_rate)
        newMpcr = False
        while not newMpcr:
            number = random.choice(Constants.MPCRS)
            if pastMpcrs.count(number) < 2:
                newMpcr = number
        self.efficiency_rate = newMpcr

    def set_payoffs(self):
        # add some logic here to add up contributions
        # from rounds 1-10, 11-20, 21-30
        x = self.session.vars['paying_round']
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * self.efficiency_rate
        for p in self.get_players():
            p.potential_payoff = (Constants.endowment - p.contribution) + self.individual_share
            p.payoff = 0

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

    def set_signal_value(self):
        mpcr = self.group.efficiency_rate
        signalVariance = self.session.config['signalVariance']
        choicesLeft = [mpcr - Decimal(x*.1) for x in range(1, signalVariance + 1)]
        choicesRight = [mpcr + Decimal(x*.1) for x in range(1, signalVariance + 1)]

        #chop off choices if at the tail
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

    def get_signal_values(self):
        if self.session.config['signalVariance'] == 2:
            signalVariance = Decimal(.2)
        else:
            signalVariance = Decimal(.1)
        left = self.signal - signalVariance
        right = self.signal + signalVariance
        signals = dict(left=left.quantize(Decimal('.01')), right=right.quantize(Decimal('.01')))
        return signals

    def set_image(self):
        playerimage = PlayerImage(participant_id=self.participant.id, image=self.image)
        playerimage.save()

    def get_game_info(self):
        for p in self.in_all_rounds():
            if p.subsession.round_number == 1:
                info = []
            info.append(p)
        return info

    def get_game_payoffs(self):
        payoffs = []
        for p in self.in_all_rounds():
            payoffs.append(p.potential_payoff)

    def get_round_period(self):
        x = 1
        for r in [1]:
            if self.subsession.round_number in range(r, r+Constants.rounds_per_game):
                game_round = self.subsession.round_number - r
                break
            else:
                x += 1
        return [game_round + 1, x]
