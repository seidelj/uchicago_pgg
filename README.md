First, you will need to have Python 3.5 installed and oTree.  oTree provides installation instructions for both in their documentation: http://otree.readthedocs.io/en/latest/install.html
NOTE: I recomend installing oTree into a virtual environment.  This will make sure you don't violate any dependencies in other projects. Additionally, environment variables will likely be required; better they are specified in the virtual env than computers profile.  Python35 comes preloaded with a package that will create virtual environments.


Initializing a virtual environment and activating it.
'''
$ pyvenv venv
$ source venv/bin/activate
'''

If you have installed python35 and it is working correctly, oTree installation boils down to
'''
(venv)$ pip3 install otree
'''



Background on getting started with Heroku: https://devcenter.heroku.com/articles/getting-started-with-python#introduction
You only need to get through the first two pages.  I'll pick up from there.

Create a virtual environment.
$ virtualenv venv

Activate
$ source venv/bin/activate

Install requirements (only if  you want to develop or deploy locally)
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


Create app at heroku.com.
-Under Settings>Reveal Config Variable add the following based on envirnment variables defined above
-- SECRET_KEY 
-- ADMIN_USERNAME
-- ADMIN_PASSWORD
-- OTREE_ACCESS_CODE
-- OTREE_AUTH_LEVEL
-- OTREE_PRODUCTION

install heroku's command line tools.  You'll will want to have you heroku app linked to the directory that contains the code to run the experiment.
$ heroku git:remote -a your_heroku_apps_name

Provision a database (reade more: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-the-add-on)
I strongly recommend standard-0, otherwise there will performance issues in the lab. https://elements.heroku.com/addons/heroku-postgresql

$ heroku addons:create heroku-postgresql:standard-0
$ heroku pg:wait
Set up the database
$ heroku run python manage.py mirgate



NOTES
Uses an old build of oTree.  Requires SQL database backends.  If you are trying to run locally or develop, you'll need psycopg2, which depends on postgres drivers.  Do your own research.
