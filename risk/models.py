# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

from decimal import *

author = 'Joe'

doc = """
Risk game based on Holt and Laury.  Ambiguity game based on mulitple choice list for risk and ambiguity.

In the risk game, player chooses which of the 5 gambles he wants to play, and a coin is "tossed" by the computer.  Payouts are below based on game chosen by player and coin toss.   The amounts are expressed in tokens (points).

Risk Gambles
    Gamble 1: Heads 36, Tails 36
    Gamble 2: 44, 32
    Gamble 3: 52, 28
    Gamble 4: 60, 24
    Gamble 5: 68, 20


In the ambiguity game.  Players make 10 choices.  In each choice, they decided which urn to pick from and which color. The computer then randomly selects one of the 10 choices, and randomly picks a color.  Players are payed based on the decisions made in that choice.

Urns
    0: ambiguous urn
    1: 50/50 urn

Balls colors in urn:
    0: Black
    1: White

"""

class Constants:
    name_in_url = 'risk'
    players_per_group = None
    num_rounds = 1

    # define more constants here
    RISKDICT = {
        '1': [36, 36],
        '2': [44, 32],
        '3': [52, 28],
        '4': [60, 24],
        '5': [68, 20],
    }

    URNDICT = {
        '1': [100, 100],
        '2': [100, 90],
        '3': [100, 80],
        '4': [100, 70],
        '5': [100, 60],
        '6': [100, 50],
        '7': [100, 40],
        '8': [100, 30],
        '9': [100, 20],
        '10': [100, 10],
    }

    URNS = {
        '1': ['0','1'],
        '0': ['0','0','0','1','1'],
    }

class Subsession(otree.models.BaseSubsession):

    app_label = models.CharField(default="risk")


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):

    risk_points = models.DecimalField(max_digits=12, decimal_places=2)

    GAMBLES = (
        ('1', "Gamble 1"),
        ('2', "Gamble 2"),
        ('3', "Gamble 3"),
        ('4', "Gamble 4"),
        ('5', "Gamble 5"),
    )

    URNS = (
        ('0', "Black: ? |  White: ?"),
        ('1', "Black:50% | White:50%"),
    )

    COLORS = (
        ('0', "Black"),
        ('1', "White"),
    )

    risk_flip = models.IntegerField(doc="The flip chosen by the computer. 0:Heads 1: Tails")

    risk_choice = models.CharField(initial=None,
        choices=GAMBLES,
        verbose_name="Choose the gamble you to play",
            doc="The coinflip gamble the subject wants to play.  Variable takes value 1,...,5 which correspond to     Gamble 1, ..., Gamble 5."
    )
    risk_payoff = models.DecimalField(max_digits=12, decimal_places=2)

    amb_chosen_game = models.CharField(doc="The game randomly choosen by the computer among the ten available.")
    amb_chosen_ball = models.CharField(doc="The ball chosen by the computer; 0: Black,1: White")
    amb_payoff = models.DecimalField(max_digits=12, decimal_places=2)
    amb_points = models.DecimalField(max_digits=12, decimal_places=2)

    amb_choice1_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice1_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice2_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice2_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice3_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice3_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice4_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice4_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice5_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice5_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice6_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice6_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice7_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice7_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice8_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice8_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice9_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice9_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )

    amb_choice10_urn = models.CharField(initial=None,
        choices=URNS,
    )
    amb_choice10_color = models.CharField(initial=None,
        choices=COLORS,
        widget=widgets.RadioSelectHorizontal(), verbose_name=""
    )


    def get_chosen_urn(self):
        urn = getattr(self, "amb_choice{}_urn".format(self.amb_chosen_game))
        if urn == "0":
            u = "Black: ? | White: ?"
        else:
            u = "Black: 50% | White: 50%"
        return u

    def get_chosen_color(self):
        color = getattr(self, "amb_choice{}_color".format(self.amb_chosen_game))
        if color == "0":
            c = "Black"
        else:
            c = "White"
        return c

    def get_drawn_color(self):
        if self.amb_chosen_ball == "0":
            color = "Black"
        else:
            color = "White"
        return color

    def set_amb_payoffs(self):
        self.amb_chosen_game = random.choice(range(1,11))
        gamble = Constants.URNDICT[str(self.amb_chosen_game)]
        urn = getattr(self, "amb_choice{}_urn".format(self.amb_chosen_game))
        color = getattr(self, "amb_choice{}_color".format(self.amb_chosen_game))
        self.amb_chosen_ball = random.choice(Constants.URNS[str(urn)])
        if self.amb_chosen_ball == color:
            self.amb_points = gamble[int(urn)]
            self.amb_payoff = self.amb_points * self.session.real_world_currency_per_point
        else:
            self.amb_points = 0
            self.amb_payoff = 0
        self.participant.vars['amb_points'] = self.amb_points
        self.participant.vars['amb_payoff'] = self.amb_payoff

    def set_risk_payoffs(self):

        flip = random.choice([0,1])
        self.risk_flip = flip
        result = Constants.RISKDICT[self.risk_choice]
        self.risk_points = result[flip]
        self.risk_payoff = Decimal(result[flip]) * self.session.real_world_currency_per_point
        self.participant.vars['risk_points'] = self.risk_points
        self.participant.vars['risk_payoff'] = self.risk_payoff

    def set_payoffs(self):
        self.payoff = sum([self.risk_payoff, self.amb_payoff])

    def flipcoin(self):
        result = random.choice([0,1])
        self.risk_flip = result

    def get_form_fields(self):
        form_fields = []
        for x in range(1, len(Constants.URNDICT) + 1):
            form_fields.append("amb_choice{}_urn".format(x))
            form_fields.append("amb_choice{}_color".format(x))
        return form_fields
