# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class SurveyIntro(Page):

    pass


class Risk(Page):

    """ Displays Participant ID number to be written on risk task """
    pass

class Demographics(Page):

    form_model = models.Player
    form_fields = [
        'q_age',
        'q_gender',
        'q_race',
        'q_education',
        'q_professional',
        'q_gpa',
    ]

    def before_next_page(self):
        # 0 Dollars
        self.player.set_payoff()

class EssayQuestions(Page):
    form_model = models.Player
    form_fields = [
        'q_decision',
        'q_comments',
    ]



page_sequence =[
        SurveyIntro,
        Demographics,
        EssayQuestions,
]
