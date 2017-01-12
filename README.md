

# A variant of the public goods game for replication.

## FIRST TIME SETUP

There are two parts to first time setup.  First, setting the project up locally.  Second, deploying the project to a server.  

### Requirements

1. Python 3.5, oTree provides installation instructions in their documentation: http://otree.readthedocs.io/en/latest/install.html.  Don't worry about installing oTree.  We'll get to that later.

2. Git (recommended).  A general idea of git and how to use it will be beneficial but it is not absolutely neccessary.  The project is hosted on github so I'll recommend this for anyone who cares: https://help.github.com/articles/set-up-git/

### Local machine setup. 

Copy or clone (` git clone git@github.com:seidelj/uchicago_pgg.git . `) this repository into an empty directory on your machine.

Create a virtual environment in the directory.  First, make sure that you are in the projects root directory. If you enter `ls` you should seed Procfile, public_goods,...,settings.py,...,manage.py,...  Next, enter the commands into your terminal.
```
$ pyvenv venv
$ source venv/bin/activate
```

If you are not familiar with virtual environments, the basic idea is that any python packages or environmental variables required will be specific and stored in the same location as this project on your local machine.  If the environment is 'active' you'll see '(venv)' on your terminal's command line. 

Deactivate your virtual environment and set some variables.
```
(venv)$ deactivate
```

In a text editor, open the file venv/bin/activate.  (The venv folder will be located in the project's root directory).  A the bottom of the file, add the following lines.

    export SECRET_KEY='your secret key'
    #GENERATE A SECRET KEY USING: http://www.miniwebtool.com/django-secret-key-generator/
    export OTREE_AUTH_LEVEL='STUDY'
    export OTREE_ADMIN_PASSWORD='password'
    
Reactivate your virtual environment.
```
$ source venv/bin/activate
```


Install neccessary Python packages to your virtual environment.
```
(venv)$ pip3 install -r requirements_base.txt
```
Check to see that everything worked.
```
(venv)$ otree resetdb
(venv)$ otree runserver
```

The instruction above, are with a Unix or Unix-Based OS in mind.  For troubleshooting or futher reference: http://otree.readthedocs.io/en/latest/install.html.

### Local machine development.

At this point, you can make any required changes and test them locally, using the the command `otree runserver` and going to http://127.0.0.1:8000/ in any webrowser.  This will be particulary useful if you want to change text displayed to subjects.

(NEED TO ADD INSTRUCTION ABOUT LOCALIZATION HERE)

### Server set up


Background on getting started with Heroku: https://devcenter.heroku.com/articles/getting-started-with-python#introduction
You only need to get through the first two pages.  I'll pick up from there.


Create app at heroku.com.
#### Under Settings>Reveal Config Variable add the following based on envirnment variables defined in venv/bin/activate
```
SECRET_KEY 
ADMIN_USERNAME
ADMIN_PASSWORD
OTREE_ACCESS_CODE
OTREE_AUTH_LEVEL
OTREE_PRODUCTION
```
install heroku's command line tools.  You'll will want to have you heroku app linked to the directory that contains the code to run the experiment.
$ heroku git:remote -a your_heroku_apps_name

Provision a database (reade more: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-the-add-on)
I recommend standard-0.   When I originally ran this experiment for Luigi et al, I ran into performance issues and errors using a lessor tear.  However, I was using an out-dated version of oTree, the current version may have improved.  If you do try to use a lesser tear, it is at your own risk.

$ heroku addons:create heroku-postgresql:standard-0
$ heroku pg:wait
Set up the database
$ heroku run python manage.py mirgate


