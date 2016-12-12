# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from .QUIZ_KEY import dict_of_dicts

class IDScreen(Page):

    form_model = models.Player
    form_fields =['label']    

class QuizIntro(Page):

    def before_next_page(self):
        self.player.set_label()    

class QuizFirst(Page):

    template_name = "quizes/Quiz.html"

    form_model = models.Player
    
    def get_form_fields(self):
        return self.player.get_form_fields(pnum=1)

    def is_displayed(self):
        return True
    
    def vars_for_template(self):
        quizDict = {}
        for key, value in dict_of_dicts['q_first'].items():
            if key != "table":
                qkey = "q_first_{}".format(key)
            else:
                qkey = key
            quizDict[qkey] = value

        return {
            'treatment': self.session.session_type['treatment'],
            'quizDict': quizDict,
        }

    def error_message(self, values):
        answers = dict_of_dicts['q_first']
        for quiz, answer in answers.items():
            qkey = "q_first_{}".format(quiz)
            if values[qkey] != answer[1]:
                return 'Atleast one of your answers is not correct'

class QuizTwo(QuizFirst):


    def get_form_fields(self):
        return self.player.get_form_fields(2)
    
    def vars_for_template(self):
        quiz = self.player.get_quiz()
        quiz = "{}_2".format(quiz)
        quizDict = {}
        for key, value in dict_of_dicts[quiz].items():
            if key != "table":
                qkey = "{}_{}".format(quiz, key)
            else:
                qkey = key
            quizDict[qkey] = value
        return {
            'tbl': True,
            'treatment': self.session.session_type['treatment'],
            'table_headers': Constants.efficiency_floats,
            'quizDict': quizDict,
        }

    def error_message(self, values):
        quiz = self.player.get_quiz()
        quiz = "{}_2".format(quiz)
        answers = dict_of_dicts[quiz]
        for question, answer in answers.items():
            if question != "table":
                qkey = "{}_{}".format(quiz, question)
                if values[qkey] != answer[1]:
                    return "Atleast one of your answers is not correct"


class QuizThree(QuizTwo):
    
    def get_form_fields(self):
        return self.player.get_form_fields(3)

    def vars_for_template(self):
        quiz = self.player.get_quiz()
        quiz = "{}_3".format(quiz)    
        quizDict = {}
        for key, value in dict_of_dicts[quiz].items():
            if key != "table":
                qkey = "{}_{}".format(quiz, key)
            else:
                qkey = key
            quizDict[qkey] = value
        return {
            'tbl': True,
            'treatment': self.session.session_type['treatment'],
            'table_headers': Constants.efficiency_floats,
            'quizDict': quizDict,
        }

    def error_message(self, values):
        quiz = self.player.get_quiz()
        quiz = "{}_3".format(quiz)
        answers = dict_of_dicts[quiz]
        for question, answer in answers.items():
            if question != "table":
                qkey = "{}_{}".format(quiz, question)
                if values[qkey] != answer[1]:
                    return "Atleast one of your answers is not correct"

class QuizWaitPage(WaitPage):
    
    wait_for_all_groups = True

    def body_text(self):
        return "Waiting for all players to complete the quiz"

page_sequence = [
    IDScreen, 
    QuizIntro,
    QuizFirst,
    QuizTwo,
    QuizThree,
    QuizWaitPage,
]




