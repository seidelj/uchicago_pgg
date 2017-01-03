# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

RACE_CHOICES = [
	'White', 'Hispanic or Latino', 'Black or African American',
	'Native American or American Indian', 'Asian / Pacific Islander',
	"Other",
]

EDUCATION_CHOICES = [
	'No schooling completed',
	'Nursery school to 8th grade',
	'Some high school, no diploma',
	'High school graduate, dimploma or the equivalent',
	'Some college credit, no degree',
	'Trade/technical/vocational training',
	'Associate degree',
	'Bacheler\'s degree',
	'Master\'s degree',
	'Professional Degree',
	'Doctorate degree',
]

HOUSEHOLD_CHOICES = [
	'Single, never married',
	'Married or domestic partnership',
	'Widowed',
	'Divorced',
	'Separated',
]

PROFESSIONAL_CHOICES = [
	'Employed for wages',
	'Self-employed',
	'Out of work and looking for work',
	'Out of work but not currently looking for work',
	'A homemaker',
	'A student',
	'Military',
	'Retired',
	'Unable to work',
]

# </standard imports>

author = 'Joe'

doc = """
Demographics Survey
"""

class Constants:
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
	# <built-in>
	subsession = models.ForeignKey(Subsession)
	# </built-in>

	def set_payoffs(self):
		for p in self.get_players():
			p.payoff = 0 # change to whatever the payoff should be

class Player(otree.models.BasePlayer):
	# <built-in>
	subsession = models.ForeignKey(Subsession)
	group = models.ForeignKey(Group, null = True)
	
	# </built-in>
	def set_payoff(self):
		self.payoff = 0

    # example field
	q_race = models.CharField(initial=None,
		choices=RACE_CHOICES,
		verbose_name="Ethnicity origin (or Race): Please specify your ethnicity"
	)
	q_age = models.PositiveIntegerField(verbose_name="What is your age?",
		choices=range(13,125),
		initial=None
	)
	q_gender = models.CharField(initial=None,
		choices = ['Female', 'Male'],
		verbose_name = "What is your gender?",
		widget = widgets.RadioSelect()
	)
	q_education = models.CharField(initial=None,
		choices=EDUCATION_CHOICES,
		verbose_name = "Education: What is the highest degree or level of school you have completed?",
	)
	q_household = models.CharField(initial=None,
		choices=HOUSEHOLD_CHOICES,
		verbose_name="Marital Status: What is your marital status",
	)
	q_gpa = models.CharField(blank=True, verbose_name="If you are a student, what is your gpa?")
	q_professional = models.CharField(initial=None,
		choices=PROFESSIONAL_CHOICES,
		verbose_name="Employment Status: Are you currenly...?",
	)
	q_decision = models.TextField(initial=None, verbose_name="Can you explain in few words what guided your decision to invest or not invest in the Group Account?")
	q_comments = models.TextField(blank=True, initial=None, verbose_name="Do you have any comment, questions, or complains about today's experiment?")

