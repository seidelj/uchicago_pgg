# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.views.generic import FormView

#CHANGE TEXT IN QUOTES FOR TRANSLATION
_RESULTS_WAIT_PAGE_TITLE_TEXT = "Please Wait"
_RESULTS_WAIT_PAGE_BODY_TEXT = "Waiting for other participants to contribute."

class Feedback(Page):
    def is_displayed(self):
        return True

class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']
    auto_submit_values = {'contribution': c(Constants.endowment/2)}

    def vars_for_template(self):
        return {
            'table_headers': Constants.efficiency_factors,
            'treatment': self.session.config['treatment'],
        }

class ResultsWaitPage(WaitPage):

    title_text = _RESULTS_WAIT_PAGE_TITLE_TEXT
    body_text = _RESULTS_WAIT_PAGE_BODY_TEXT

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    timeout_seconds = 15
    """Players payoff: How much each has earned"""
    def before_next_page(self):
        if self.subsession.round_number == Constants.num_rounds:
            self.player.set_session_payoffs()

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * self.group.efficiency_rate,
            'individual_earnings': self.player.round_points,
            'treatment': self.session.config['treatment'],
        }

class ResultsSummary(Page):

    def is_displayed(self):
        r = Constants.rounds_per_game
        return self.subsession.round_number in [r, r*2, r*3, r*4]

    def vars_for_template(self):

            if self.session.vars['paying_round'] == 1:
                paying_round = "Game 1"
            elif self.session.vars['paying_round'] == 9:
                paying_round = "Game 2"
            elif self.session.vars['paying_round'] == 17:
                paying_round = "Game 3"
            elif self.session.vars['paying_round'] == 25:
                paying_round = "Game 4"

            varied = self.session.vars['varied_round'] + (Constants.rounds_per_game -1) == self.subsession.round_number

            return {
                'varied': varied,
                'treatment': self.session.config['treatment'],
                'info': self.player.get_game_info(),
                'payoff' : self.player.get_game_payoffs(),
                'paying_round': paying_round,
                'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
            }

class NewGame(Page):

    timeout_seconds = 20

    def is_displayed(self):
        return self.subsession.round_number in Constants.starting_rounds

    def vars_for_template(self):
        x = 0
        for r in Constants.starting_rounds:
            if self.subsession.round_number in range(r, r+Constants.rounds_per_game):
                game_number = x + 1
                break
            else:
                x += 1
        return {
            'period': game_number,
            'varied': self.session.vars['varied_round'] == self.subsession.round_number,
        }

page_sequence = [
            NewGame,
            Contribute,
            ResultsWaitPage,
            Results,
            ResultsSummary,
    ]
