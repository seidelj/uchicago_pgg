# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

from .QUIZ_KEY import dict_of_dicts
# </standard imports>
from django.utils import timezone

author = 'Joe Seidel'

doc = """
Questions testing comprehension of instructions.  This data will not be useful because subjects are not allowed to advance unless all questions are answered correctly.
"""

class Constants:
    name_in_url = 'quizes'
    players_per_group = None
    num_rounds = 1

    efficiency_floats = [
        .05, .15, .25,
        .35, .45, .55, .65,
        .75, .85, .95, 1.05,
        1.15, 1.25,
    ]


class Subsession(otree.models.BaseSubsession):

    app_label = models.CharField(default="quizes")

class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):

    PRIVATE_CHOICES_2 = (
        ("1", "0.45, 0.55, 0.65"),
        ("2", "0.25, 0.35, 0.45"),
        ("3", "0.35, 0.45, 0.55"),
    )

    PRIVATE_CHOICES_3 = (
        ("1", "0.95, 1.05, 1.15"),
        ("2", "0.85, 0.95, 1.05"),
        ("3", "0.75, 0.85, 0.95"),
    )

    PUBLIC_CHOICES_2 = (
        ("1", "1.05, 1.15, 1.25"),
        ("2", "0.95, 1.05"),
        ("3", "1.05"),
    )

    PUBLIC_CHOICES_3 = (
        ("1", "0.95, 1.05, 1.15"),
        ("2", "1.05, 1.15"),
        ("3", "1.05, 1.15, 1.25"),
    )

    PRIVATE_WIDE_CHOICES_2 = (
        ("1", "0.05, 0.15, 0.25, 0.35, 0.45"),
        ("2", "0.55, 0.65, 0.75, 0.85, 0.95"),
        ("3", "0.25, 0.35, 0.45, 0.55, 0.65"),
    )

    PRIVATE_WIDE_CHOICES_3 = (
        ("1", "0.55, 0.65, 0.75, 0.85, 0.95"),
        ("2", "0.75, 0.85, 0.95, 1.05, 1.15"),
        ("3", "0.65, 0.75, 0.85, 0.95, 1.05"),
    )

    PUBLIC_WIDE_CHOICES_2 = (
        ("1", "0.85, 0.95, 1.05, 1.15, 1.25"),
        ("2", "1.05, 1.15, 1.25"),
        ("3", "0.85, 0.95, 1.05"),
    )

    PUBLIC_WIDE_CHOICES_3 = (
        ("1", "0.55, 0.65"),
        ("2", "0.35, 0.45, 0.55"),
        ("3", "0.25, 0.35, 0.45. 0.55, 0.65"),
    )

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    label = models.CharField()
    q_first_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    q_first_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    q_first_q3 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    q_first_q4 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    q_first_q5 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    q_first_q6 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_2_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_2_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_2_q3 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_2_q4 = models.CharField(initial=None, choices=PRIVATE_CHOICES_2, widget=widgets.RadioSelect())
    private_3_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_3_q2 = models.CharField(initial=None, choices=PRIVATE_CHOICES_3, widget=widgets.RadioSelect())
    exact_2_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    exact_3_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_2_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_2_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_2_q3 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_2_q4 = models.CharField(initial=None, choices=PUBLIC_CHOICES_2, widget=widgets.RadioSelect())
    public_3_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_3_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_3_q3 = models.CharField(initial=None, choices=PUBLIC_CHOICES_3, widget=widgets.RadioSelect())

    private_wide_2_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_wide_2_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_wide_2_q3 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_wide_2_q4 = models.CharField(initial=None, choices=PRIVATE_WIDE_CHOICES_2, widget=widgets.RadioSelect())
    private_wide_3_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    private_wide_3_q2 = models.CharField(initial=None, choices=PRIVATE_WIDE_CHOICES_3, widget=widgets.RadioSelect())

    public_wide_2_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_wide_2_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_wide_2_q3 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_wide_2_q4 = models.CharField(initial=None, choices=PUBLIC_WIDE_CHOICES_2, widget=widgets.RadioSelect())
    public_wide_3_q1 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_wide_3_q2 = models.CharField(initial=None, choices=['True', 'False'], widget=widgets.RadioSelect())
    public_wide_3_q3 = models.CharField(initial=None, choices=PUBLIC_WIDE_CHOICES_3, widget=widgets.RadioSelect())

    def set_label(self):
        self.participant.label = self.label
        self.label = ""

    def get_quiz(self):
        treatment = self.session.config['treatment']
        signalVariance = self.session.config['signalVariance']
        if treatment == 1:
            quiz = "exact"
        elif treatment == 2 or treatment == 4:
            quiz = "private"
        elif treatment == 3 or treatment == 5:
            quiz = "public"
        else:
            quiz = "NONE"

        if treatment == 2 and signalVariance == 2:
            quiz = "private_wide"
        elif treatment == 3 and signalVariance == 2:
            quiz = "public_wide"
        else:
            pass
        return quiz

    def get_form_fields(self, pnum):
        form_fields = []
        if pnum == 1:
            for x in range(1, len(dict_of_dicts['q_first']) + 1):
                form_fields.append("q_first_q{}".format(x))
        else:
            quiz = self.get_quiz()
            quiz = "{}_{}".format(quiz, pnum)
            for x in range(1, len(dict_of_dicts[quiz])):
                form_fields.append("{}_q{}".format(quiz, x))
        return form_fields


