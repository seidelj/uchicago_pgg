#-*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .forms import ImageForm

class TrainingIntro(Page):
	
	def is_displayed(self):
		return self.subsession.round_number == 1

class UploadImage(Page):
	
	def is_displayed(self):
		pt = self.player.treatment
		uploads = False
		if pt == 4 or pt == 5:
			uploads = True
		return self.subsession.round_number == 1 and uploads

	def vars_for_template(self):
		return {
			'imageform': ImageForm,
		}

	def before_next_page(self):
		self.player.set_image()

	form_model = models.Player
	form_fields = ['image']

class Contribute(Page):

	form_model = models.Player
	form_fields = ['contribution']
	auto_submit_values = {'contribution': c(Constants.endowment/2)}	

	def vars_for_template(self):
		return {
			'practice': True,
			'table_headers': Constants.efficiency_factors,
			'treatment': self.session.session_type['treatment'],
		}

class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		self.group.set_payoffs()

	def body_text(self):
		return "Waiting for other participants to contribute"

class TrainingWaitPage(WaitPage):

	wait_for_all_groups = True

	def is_displayed(self):
		return self.subsession.round_number == Constants.num_rounds

	def body_text(self):
		return "Waiting for other players to finish the training period"

class Results(Page):
	
	timeout_seconds = 15

	def vars_for_template(self):
		return	{
			'practice': True,
			'total_earnings': self.group.total_contribution * self.group.efficiency_rate,
			'individual_earnings': self.player.potential_payoff,
			'treatment': self.session.session_type['treatment'],
		}

class ResultsSummary(Page):
	
	def is_displayed(self):
		return self.subsession.round_number == 4

	def vars_for_template(self):
		paying_round = "Practice Game Results"

		return {
			'practice': True,
			'treatment': self.session.session_type['treatment'],
			'info': self.player.get_game_info(),
			'payoff': self.player.get_game_payoffs(),
			'paying_round': paying_round,
			'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
		}

class TrainingConclusion(Page):
	
	def is_displayed(self):
		return self.subsession.round_number == Constants.num_rounds


page_sequence = [
	TrainingIntro,
	UploadImage,
	Contribute,
	ResultsWaitPage,
	Results,
	ResultsSummary,
	TrainingWaitPage,
	TrainingConclusion,
]

