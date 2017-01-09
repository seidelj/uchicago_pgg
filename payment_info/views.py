# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from decimal import *

class PaymentInfo(Page):

	def vars_for_template(self):
		participant = self.player.participant
		pg_payoff = self.player.participant.vars['pg_payoff']
		risk_payoff = self.player.participant.vars['risk_payoff']
		amb_payoff = self.player.participant.vars['amb_payoff']
		amb_points = self.player.participant.vars['amb_points']
		pg_points = self.player.participant.vars['pg_points']
		risk_points = self.player.participant.vars['risk_points']
		pr = self.session.vars['paying_round']
		if pr == 1:
			game = "Game 1"
		elif pr == 9:
			game = "Game 2"
		elif pr == 17:
			game = "Game 3"
		elif pr == 25:
			game = "Game 4"
		else:
			game = None

		return {
			'participant': participant,
			'game': game,
			'pg_points': pg_points,
			'pg_payoff': pg_payoff,
			'risk_points': risk_points,
			'risk_payoff': risk_payoff,
			'additional_points': sum([risk_points, amb_points]),
			'points': sum([risk_points, pg_points, amb_points]),
			'money': sum([risk_payoff, pg_payoff, amb_payoff]),
			'takehome': sum([amb_payoff, risk_payoff, pg_payoff, Decimal(10)]),
		}

page_sequence = [PaymentInfo]
