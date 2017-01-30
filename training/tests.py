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
        if self.subsession.round_number == 1:
            yield (views.TrainingIntro)
        pt = self.player.treatment
        uploads = False
        if pt == 4 or pt ==5: uploads = True

        if self.subsession.round_number == 1 and uploads:
            yield (
                views.UploadImage, {
                    'image': 'https://s3.amazonaws.com/labgames/uploads/imgs/photo+1.JPG',
                }
            )

        yield (
            views.Contribute, {
                "contribution": random.choice(range(0, Constants.template_endowment))
            }
        )

        yield (views.Results)

        if self.subsession.round_number == 4:
            yield (views.ResultsSummary)
            yield (views.TrainingConclusion)


    def validate_play(self):
        pass
