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
		context = {}
		for x in range(1, 11):
			urnkey = "amb_choice{}_urn".format(x)
			colorkey = "amb_choice{}_color".format(x)
			context[urnkey] = "0"
			context[colorkey] = "0"
		
		self.submit(views.RiskIntro)
		self.submit(views.Risk, {'risk_choice': '3'})
		self.submit(views.Ambiguity, context)
		self.submit(views.WaitPage)
		self.submit(views.Results)

	def validate_play(self):
		pass
