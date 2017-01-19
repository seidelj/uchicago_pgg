#-*- coding: utf-8 -*-
from __future__ import division
from otree.common import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


#CHANGE TEXT IN QUOTES FOR TRANSLATION
_RESULTS_WAIT_PAGE_TITLE_TEXT = "Please Wait"
_RESULTS_WAIT_PAGE_BODY_TEXT = "Waiting for other participants to contribute."
_TRAINING_WAIT_PAGE_TITLE_TEXT = "Please Wait"
_TRAINING_WAIT_PAGE_BODY_TEXT = "Waiting for other players to finish the training period"


class TrainingIntro(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

class Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']
    auto_submit_values = {'contribution': c(Constants.endowment/2)}

    def vars_for_template(self):
        return {
            'practice': True,
            'table_headers': Constants.efficiency_factors,
            'treatment': self.session.config['treatment'],
        }

class ResultsWaitPage(WaitPage):

    title_text = _RESULTS_WAIT_PAGE_TITLE_TEXT
    body_text = _RESULTS_WAIT_PAGE_BODY_TEXT

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class TrainingWaitPage(WaitPage):

    wait_for_all_groups = True

    title_text = _TRAINING_WAIT_PAGE_TITLE_TEXT
    body_text = _TRAINING_WAIT_PAGE_BODY_TEXT

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


class Results(Page):

    timeout_seconds = 15

    def vars_for_template(self):
        return    {
            'practice': True,
            'individual_earnings': self.player.round_points,
            'treatment': self.session.config['treatment'],
        }

class ResultsSummary(Page):

    def is_displayed(self):
        return self.subsession.round_number == 4

    def vars_for_template(self):
        return {
            'practice': True,
            'treatment': self.session.config['treatment'],
            'info': self.player.get_game_info(),
            'payoff': self.player.get_game_payoffs(),
            'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
        }

class TrainingConclusion(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [
    TrainingIntro,
    Contribute,
    ResultsWaitPage,
    Results,
    ResultsSummary,
    TrainingWaitPage,
    TrainingConclusion,
]
