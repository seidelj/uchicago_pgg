"""
Django settings for labgames project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

from boto.mturk import qualification
import otree.settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get("MYAPP_DEBUG", False)
if os.environ.get('OTREE_PRODUCTION') in {None, '', '0'}:
    DEBUG = True
else:
    DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')
ACCESS_CODE_FOR_DEFAULT_SESSION = os.environ.get('OTREE_ACCESS_CODE')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY","")

PAGE_FOOTER = ''

DATABASES = {
	'default': dj_database_url.config()
}


# settting for intergration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

INSTALLED_APPS = [
	'otree',
	's3direct',
]

AWS_STORAGE_BUCKET_NAME = 'labgames'

S3DIRECT_REGION = 'us-east-1'

S3DIRECT_DESTINATIONS = {
	'imgs': ('uploads/imgs', lambda u: True, ['image/jpeg', 'image/png'],),
	}

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]


DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

########################################################################################
######From here is mturk stuff that I included to keep the otree-core package happy#####
########################################################################################

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# a`nd also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification


mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        #qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.05,
    'participation_fee': 10.00,
    'num_bots': 16,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': mturk_hit_settings
}


BASE_SESSION_CONFIGS = [
    {
        'name': 'public_goods_1',
        'display_name': "Public Goods Exact",
        'num_demo_participants': 4,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        'treatment': 1,
        'mpcrOrder': 1,
        'signalVariance': 0,
    },
    {
        'name': 'public_goods_2',
        'display_name': "Public Goods Private Signal-Narrow",
        "num_demo_participants": 4,
        "app_sequence": ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        'treatment': 2,
        'mpcrOrder': 2,
        'signalVariance': 1,
    },
    {
        'name': 'public_goods_3',
        'display_name': "Public Goods Public Signal-Narrow",
        'num_demo_participants': 4,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk', 'survey', 'payment_info'],
        'treatment': 3,
        'mpcrOrder': 3,
        'signalVariance': 1,
    },
    {
        'name': 'public_goods_6',
        'display_name': "Public Goods Private Signal-Wide",
        'num_demo_participants': 4,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk',  'survey', 'payment_info'],
        'treatment': 2,
        'mpcrOrder': 1,
        'signalVariance': 2,
    },
    {
        'name': 'public_goods_7',
        'display_name': "Public Goods Public Signal-Wide",
        'num_demo_participants': 4,
        'app_sequence': ['quizes', 'training', 'public_goods', 'risk',  'survey', 'payment_info'],
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


otree.settings.augment_settings(globals())
ROOT_URLCONF = 'urls'
