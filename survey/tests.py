# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	"""Bot that plays one round"""
	
	def play_round(self):
		self.submit(views.SurveyIntro)
		self.submit(views.Demographics, {
			'q_age': 27,
			'q_gender': "Male",
			'q_race': "White",
			'q_education': "Bacheler\'s degree",
			"q_professional": "Employed for wages",
			"q_gpa": "2.1",
		})
		self.submit(views.EssayQuestions, {
			'q_decision': "Close my eyes",
			'q_comments': "Great programming",
		})

	def validate_play(self):
		pass
