# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time


class RiskIntro(Page):

    pass


class Risk(Page):
    form_model = models.Player
    form_fields = ['risk_choice']
    auto_submit_values = {'risk_choice': "1"}

    def is_displayed(self):
        return True

    def vars_for_template(self):
        gambles = []
        for key, value in Constants.RISKDICT.items():
            gambles.append(dict(name=key, value=value))
        gambles = sorted(gambles, key=lambda k: k['name'])

        return {
            'gambles': gambles,
        }

class WaitPage(Page):
    def body_text(self):
        return "Please wait while the computer determines the coin flip and selects a choice for the urns."

    def is_displayed(self):
        return True

    def before_next_page(self):
        self.player.set_risk_payoffs()
        self.player.set_amb_payoffs()
        self.player.set_payoffs()


class Ambiguity(Page):
    form_model = models.Player

    def get_form_fields(self):
        form_fields = []
        for x in range(1, 11):
            form_fields.append("amb_choice{}_color".format(x))
        for x in range(1, 11):
            form_fields.append("amb_choice{}_urn".format(x))
        return form_fields

    def vars_for_template(self):
        return {
            'choicenumber': [x for x in range(1,11)],
            'listoffields': self.player.get_form_fields(),
            'urndict': Constants.URNDICT,
        }

class Results(Page):

    def vars_for_template(self):
        gambles = []
        for key, value in Constants.RISKDICT.items():
            gambles.append(dict(name=key, value=value))
        gambles = sorted(gambles, key=lambda k: k['name'])

        return {
            'results': True,
            'gambles': gambles,
        }


page_sequence =[
        RiskIntro,
        Risk,
        Ambiguity,
        WaitPage,
        Results
]
