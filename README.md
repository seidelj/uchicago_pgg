

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


Create app at heroku.com.  Once you do this, Heroku will provide instructions on how to deploy.  The Heroku instructions will include a link to download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).  After installing the CLI, you can follow the instructions (they are repeated from Heroku) below.

##### Create a new repository
```
(venv)$ heroku login
(venv)$ git init
(venv)$ heroku git:remote -a secure-sands-26521
```

##### Deploy the application
You can follow this sequence of commands any time you might change the code and want to upload to the server.
```
(venv)$ git add .
(venv)$ git commit -am "first deploy"
(venv)$ git push heroku master
```

#### Set config variables and Heroku add-ons
Although you have deployed your local files to the server, the heroku application will not be working.  If your terminal reports an error deploying, that is also okay for now.

##### Set config varibles.
```
(venv)$ heroku config:set OTREE_PRODUCTION=1
(venv)$ heroku config:set OTREE_AUTH_LEVEL=STUDY
(venv)$ heroku config:set SECRET_KEY="SECRET KEY FROM venv/bin/activate"
(venv)$ heroku config:set OTREE_ADMIN_PASSWORD=PASSWORD_FROM_venv/bin/activate
```
Now, you should be able to successfully deploy to heroku.
```
(venv)$ git push heroku master
```

##### Install Heroku Redis add-on
```
(venv)$ heroku addons:create heroku-redis:hobby-dev
```
##### Install Heroku Postgresql add-on
A note on this:  When I first ran this project I used a much older version of oTree that required a standard-0 tier of postgres.  I will recommend the same, however for those faced with budget constraints, oTree has improved their performance and you may be able to function with a hobby-basic.  I'd certainly pilot or test with some RAs before deciding to use the lesser tier.
```
(venv)$ heroku addons:create heroku-postgresql:standard-0
Creating heroku-postgresql:standard-0 on ⬢ secure-sands-26521... $50/month
Your add-on is being provisioned and will be available shortly
Created postgresql-curved-47346 as HEROKU_POSTGRESQL_CHARCOAL_URL

(venv)$ heroku pg:wait
(venv)$ heroku pg:promote HEROKU_POSTGRESQL_CHARCOAL
```
In the last command above, replace 'CHARCOAL' with whatever color heroku tells you.

Heroku documentations for provisioning databases: [doc](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-the-add-on).
##### Initialize otree models to database
This is a destructive process, don't do this more than once unless you know what you are doing.
```
(venv)$ heroku run otree resetdb
```

#### A few last steps.
From your heroku apps dashboard, you should uprade your dynos from the resources tab.   In the original experiment, I used 1x Professional Dynos.  Make sure you activate a dyno for the "worker".   Use a lower-tiered dyno at your own risk.

At this point, you are ready to run the experiment in the lab!

## Running in the lab.

1. On a computer that will not be used by a subject log in at create a session.
(Admin Login username is set in settings.py default is admin.  Password is set as an envronment variable `OTREE_ADMIN_PASSWORD`.)
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/step1.png" width="500"/>
<br />
2. Select "+Create new session"
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/step2.png" width="500"/>
<br />
3. Select session config.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/step3.png" width="500"/>
<br />
4. Enter 16 participants, then click "Create"
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/step4.png" width="500"/>
<br />
5. Distribute links to the subject's computers.  You can either use the "Session-wide link".  Make sure you enter this link on computers 1 and a time.  If the link is initialized simultaniously on two seperate computers you may end up assiging two players to the same participant session.  OR you can use a unique link on each computer.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/step5.png" width="500"/>
<br />
You can monitor the session.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/monitor.png" width="500" />
<br />
When all subjects have finished the payments tab will report earnings.  Make sure that the lab monitor refreshes the page before paying each subject.  The values do not update otherwise.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/payments.png" width="500" />


## Exporting Data

You can download CSV or Excel files containing the data from each session.  There is also useful documentation associated with each app.

1. Click on "Data" in the page heading.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/export1.png" width="500" />

2. Click to download app data and documentation.
<br />
<img src="https://s3.amazonaws.com/labgames/instructions/export2.png" width="500" />
