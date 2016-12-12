Create a virtual environment
$ virtualenv venv

Activate
$ source venv/bin/activate

Install requirements
$ pip install -r requirements.txt

    export ADMIN_USERNAME='pick_a_username'
    export ADMIN_PASSWORD='pick_a_password'
    #Set this because oTree wants a value, but I don't recall
    #ever using it
    export OTREE_ACCESS_CODE='make_something_up'
    export OTREE_AUTH_LEVEL="DEMO"
    export OTREE_PRODUCTION='1'
    #GENERATE ONE http://www.miniwebtool.com/django-secret-key-generator/
    #DO NOT share
    export SECRET_KEY='your secret key'

NOTES
Uses an old build of oTree.  Requires SQL database backends.  If you are trying to run locally or develop, you'll need psycopg2, which depends on postgres drivers.  Do your own research.
