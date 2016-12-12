# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants
from .views import dict_of_dicts

class PlayerBot(Bot):

	"""Bot that plays one round"""
	
	def get_answers(self, pnum):
		quiz = self.player.get_quiz()
		if pnum == 1:
			quiz = "q_first"
		else:
			quiz = "{}_{}".format(quiz, pnum)
		answers = dict_of_dicts[quiz]
		answerDict = {}
		for key, value in answers.items():
			if key != "table":
				nkey = "{}_{}".format(quiz, key)
				answerDict[nkey] = value[1]
		return answerDict

	def play_round(self):
		self.submit(views.IDScreen, {'label': "joe"})
		self.submit(views.QuizIntro)
		self.submit(views.QuizFirst, self.get_answers(1))
		self.submit(views.QuizTwo, self.get_answers(2))
		self.submit(views.QuizThree, self.get_answers(3))

	def validate_play(self):
		pass
