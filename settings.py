import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = environ.get('SECRET_KEY')

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
#AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.050,
    'participation_fee': 10.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}


BASE_SESSION_CONFIGS = [
    {
        'name': 'public_goods_1',
        'display_name': 'Public Goods Baseline',
        'num_demo_participants': 16,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        #'app_sequence': ['training', 'public_goods'],
        'treatment': 1,
        'mpcrOrder': 1,
        'signalVariance': 0,
    },
    {
        'name': 'public_goods_2',
        'display_name': 'Public Goods Private Signal-Thin',
        'num_demo_participants': 16,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        #'app_sequence': ['training', 'public_goods'],
        'treatment': 2,
        'mpcrOrder': 2,
        'signalVariance': 1,
    },
    {
        'name': 'public_goods_3',
        'display_name': 'Public Goods Public Signal-Thin',
        'num_demo_participants': 16,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        #'app_sequence': ['training', 'public_goods'],
        'treatment': 3,
        'mpcrOrder': 3,
        'signalVariance': 1,
    },
    {
        'name': 'public_goods_6',
        'display_name': 'Public Goods Private Signal-Thick',
        'num_demo_participants': 16,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        #'app_sequence': ['training', 'public_goods'],
        'treatment': 2,
        'mpcrOrder': 1,
        'signalVariance': 2,
    },
    {
        'name': 'public_goods_7',
        'display_name': 'Public Goods Public Signal-Thick',
        'num_demo_participants': 16,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        #'app_sequence': ['training', 'public_goods'],
        'treatment': 3,
        'mpcrOrder': 1,
        'signalVariance': 2,
    },
]

SESSION_CONFIGS = []
for baseSession in BASE_SESSION_CONFIGS:
    if baseSession['treatment'] != 4 and baseSession['treatment'] != 5:
        for x in range(1, 5):
            session = {}
            session['name'] = "{}_{}".format(baseSession['name'], x)
            session['display_name'] = baseSession['display_name'] + " -- ORDER {}".format(x)
            session['num_demo_participants'] = baseSession['num_demo_participants']
            session['app_sequence'] = baseSession['app_sequence']
            session['treatment'] = baseSession['treatment']
            session['mpcrOrder'] = x
            session['signalVariance'] = baseSession['signalVariance']
            SESSION_CONFIGS.append(session)
    else:
        SESSION_CONFIGS.append(baseSession)

RISK_CONFIG = {
    'name': "risk",
    'display_name': 'Risk Games',
    'num_demo_participants': 1,
    'app_sequence': ['risk', 'payment_info'],
}

#SESSION_CONFIGS.append(RISK_CONFIG)

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
