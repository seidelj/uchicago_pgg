# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):
    def play_round(self):

        if self.subsession.round_number in Constants.starting_rounds:
            self.submit(views.NewGame)

        self.submit(
            views.Contribute, {
                "contribution": random.choice(range(0, Constants.template_endowment+1))
            }
        )
        self.submit(views.Results)

        if self.subsession.round_number in [8, 16, 24, 32]:
            self.submit(views.ResultsSummary)

    def validate_play(self):
        pass
