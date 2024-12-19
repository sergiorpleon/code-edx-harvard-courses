# Web application for event tracking in development
#### Video Demo:  [Video show Web application for event tracking in development](https://youtu.be/tuH9zVq6K6A)
#### Description:
Project consists of creating a web application to track an event "minute by minute". Similar to the one that Marca (http://www.marca.com) uses to follow football matches on its website, and other events such as the transfer market, elections, current events in progress, etc.

In the application, a journalist creates an event and within it creates narratives of what happens in the game (if it is a football game). You can also create a survey with up to a maximum of 5 options, in which all users who log in can participate.

Users who access the event see the list of narrations made and can participate in the survey if they log in.

Users can comment, you must be logged in to do so. You can also see the last 10 comments, and if you want to continue reading more comments, click on the more comments button (it is only shown whenever there are more comments to show) and it will load the next ten comments.

If the journalist adds new narration, an update button will appear for all users who are following the event.

#### Project structure:
project
+app
 +forms		This directory contains the forms used in the application to handle user data entry.
  |-comment_forms.py 	Define the Comment form
  |-event_forms.py		Define the Category(of events) form and Event form
  |-ocurrence_forms.py	Define the EventOcurrence(used for servey or narration type) form and survey option form
  |-user_forms.py		Define the Login, Register and User form
  |-__init__.py
 +models		This directory contains the models definition used in the application.
  |-comment.py			Define the Comment model
  |-event.py				Define the Category(of events) model and Event model
  |-ocurrence.py			Define the EventOcurrence(used for servey or narration type) model and EventOcurrenceType enum
  |-survey.py			Define the SurveyOtion model and SurveyResponse model
  |-user.py				Define User model and Role model
  |-__init__.py
 +routes		This directory contains the application routes, which handle HTTP requests and responses.
  |-basic_routes.py
  |-comment_routes.py		Contains the routes related to comment management(create comment, delete comment and load more comment)
  |-event_routes.py			Contains the routes related to event management(list events of categy, create category, delete category, home, list event, create event, edit event, delete event and view event)
  |-ocurrence_routes.py		Contains the routes related to event ocurrence management(create event ocurrence, edit event ocurrence, delete event ocurrence, view survey and vote survey)
  |-user_routes.py			Contains the routes related to user management(login, logout, register, create user, edit user, delete user, view user and list users)
  |-__init__.py
 +static
 +templates	This directory contains the HTML templates that are used to render the application's views.
  |-category.html		Template to display information about events of category
  |-events.html			Template to display information about list events
  |-index.html			Template to display information events in home page
  |-layout.html
  |-login.html			Template to display login form
  |-partial_comments.html Template to display comments
  |-register.html		Template to display register form
  |-survey.html			Template to display survey information
  |-update_category.html	Template to display category form(create)
  |-update_event.html	Template to display event form(create, edit)
  |-update_ocurrence.html Template to display ocurrence form(create, edit)
  |-update_user.html		Template to display user form(edit)
  |-users.html			Template to display information about list of users
  |-view_event.html		Template to display information about event(show all narration of events)
  |-view_user.html		Template to display information about user
 |-config.py				Configuration file that defines the settings necessary for the application, such as database connection, secret keys, and security settings.
 |-helpers.py			It contains auxiliary functions that can be used in different parts of the application to avoid code duplication.
 |-__init__.py			Allows the root directory of the application to be treated as a Python package. Includes application initializations and environment configuration.
+tests		Folder with files to test. Basic admin user testing
 |-test?auth.py
 |-test_comments.py
 |-test_events.py
 |-test_ocurrence-py
|-README.md
|-requirements.txt
|-run.py

#### How to run the project:
pip install -r requirements.txt

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

python run.py

By default the application will create an administrator user with username: admin and password: admin
