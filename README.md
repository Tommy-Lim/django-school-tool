# Creating a School Tool Website with Django

We're doing to build a website for a school that allows us to keep
track of courses, staff and students. We'll create a page where
people can come to the school website and see what's courses are
currently being offered. The site will include an administrative
interface where webmasters can CRUD (create, read, update, delete)
everything in teh system.

## Start the Project
Django has a concept of "projects" and "apps." A project is a collection
of apps. Django won't let you have a project and an app with the same name.
I personally find it a good practice to keep simple projects and apps with
generally the same name, with "site" appended to the top-level "project."

Most of my Django work involves projects with only one app.

**Project Name:** "schooltoolsite"

**App Name:** "schooltool"

```bash
django-admin startproject schooltoolsite
cd schooltoolsite
python3 manage.py startapp schooltool
```

## Configure the Project
We have to manually add the schooltool app to the schooltoolsite project.

Edit the file at `schooltoolsite/settings.py`. Change INSTALLED_APPS to
include a reference to `SchooltoolConfig`. You can see `SchooltoolConfig`
defined inside `schooltoolsite/schooltool/apps.py`.

Notice that "tool" in `SchooltoolConfig` is not capitalized.

**schooltoolsite/settings.py:**
```python
INSTALLED_APPS = [
    'schooltool.apps.SchooltoolConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

### Configure the Database and Time Zone
Scroll through `schooltoolsite/settings.py` and look for where the database
is configured. Django uses a local sqlite database by default. Let's change
this to use a local postgresql database.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'schooltools',
        'HOST': 'localhost'
    }
}
```

While we're in **settings.py** scroll down a bit further to configure the
`TIME_ZONE`. There's a long list of pre-defined time zones built and maintained
by an organization called IANA (Internet Assigned Numbers Authority). They
do the hard work of figuring out how real-world messy time zone should be
represented inside computers and we can simply refer to one of their official
zone names and Django and our database will figure everything out.

The closest official time zone name for Seattle and the West Coast is
'America/Los_Angeles'. Use this.

```python
TIME_ZONE = 'America/Los_Angeles'
```

If you want to nerd out on the entire list of time zones available in this
list, and want to know more about the time zone database or IANA then go
read up on all these things on Wikipedia. This knowledge isn't really
required for any project or job, but it's good to get a sense of who all
is out there in the world of programming and how much work it takes to
keep things up and running.

* <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>
* <https://en.wikipedia.org/wiki/Tz_database>
* <https://en.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority>

## Start the Server
Start the server to see if you've made any silly mistakes so far.

Make sure you're in the directory called "schooltoolsite" and run the
runserver command:

```bash
cd /path/to/schooltoolsite
python3 manage.py runserver
```

You'll see something like this:

```bash
Performing system checks...

System check identified no issues (0 silenced).
January 30, 2017 - 03:39:45
Django version 1.10.5, using settings 'schooltoolsite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

If you see errors you'll have to track down what's wrong and fix it.

If everything is configured correctly you'll see a website that says,
"It worked!" and it will give you advice about what it thinks you should
do next.


## Customize Layout
Let's carve out some initial template and layout infrastructure. We won't
be able to see these pages yet, we'll hook up URL routing next.

* Create a folder called `static` in schooltool
	* Create a folder called `schooltool` in the new `static` dir.
    * Create a file called `style.css` in `static/schooltool`
	  * Create a folder called `images` in `static/schooltool`
      * Put an image called `background.jpg` in the images folder.
* Create a folder `templates` in schooltool and create a folder called `schooltool`
  inside that.
  * Create a file called `base.html` in `schooltool/templates/schooltool`
  * Create a file called `index.html` in `schooltool/templates/schooltool`

At the end, you should have all these folders and files:

```bash
./schooltool/static/
./schooltool/static/schooltool/
./schooltool/static/schooltool/style.css
./schooltool/static/schooltool/images/
./schooltool/static/schooltool/images/background.jpg
./schooltool/templates/
./schooltool/templates/schooltool/
./schooltool/templates/schooltool/base.html
./schooltool/templates/schooltool/index.html
```

### Pieces of Django Magic
As web developers it's important for us to understand **what** is doing *what*.
Generally, what we're doing here is writing HTML pages, using CSS to style
that HTML, and referencing an image that exists somewhere. Let's break down
where the Django magic happens:

The CSS file has no special Django magic. It includes one URL that points to
a background image. There's nothing special about this URL. The URL depends
on us configuring our static folder how Django expects.

The `base.html` file has some Django magic in it. First, notice that the
very first line looks like this:

```python
{% load static %}
```

This statement grants the `body.html` template access to some special functions
that will allow it to refer to files inside the static directory. It uses the
`static` library that it loaded to attach a href attribute to bring in the CSS.

```python
<link href="{% static 'schooltool/style.css' %}" rel="stylesheet">
```

The `base.html` file has one more piece of Django magic called a **template block**.
A template block basically defines where content from other templates will be
rendered inside of this template. The template block defines itself with a
name, so in the future other templates can fill themselves in in different parts
of the page.

Notice that our **base.html** file defines the basic structure for a classic HTML
pagee then usese the content block to define where other template will be
rendered inside the page. The **index.html** file starts out by saying that it
*extends* from the **base.html** page and it has it's own template block with
the same name, "content," surrounding all of the HTML that it will fill in on
the **base.html** page.

Summary of **base.html**
```html
<html>
  <head></head>
  <body>
    <div class="container">
      <div class="row">
        <div class="col-xs-12">
          {% block content %}
          {% endblock %}
        </div>
      </div>
    </div>
  </body>
</html>
```

Summary of **index.html**
```html
{% extends 'schooltool/base.html' %}

{% block content %}
<h1>Index</h1>
<p>Welcome to school tool</p>
{% endblock %}
```

### Literal File Contents
Here's what all of your files should look like:

**schooltoolsite/schooltool/static/schooltool/style.css**
```css
body {
  background: url('images/background.jpg') no-repeat center center fixed;
  background-size: cover;
}

.container {
  background-color: white;
  margin: 1em;
  padding: 1em;
}
```

**schooltoolsite/schooltool/templates/schooltool/base.html**
```html
{% load static %}

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>School Tool</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap-theme.min.css" rel="stylesheet" crossorigin="anonymous">
    <link href="{% static 'schooltool/style.css' %}" rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="col-xs-12">
          <nav>
            <a href="{% url 'index' %}">
              Home
            </a>
          </nav>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-xs-12">
          {% block content %}
          {% endblock %}
        </div>
      </div>
    </div>
  </body>
</html>
```

**schooltoolsite/schooltool/templates/schooltool/index.html**
```html
{% extends 'schooltool/base.html' %}

{% block content %}
<h1>Index</h1>
<p>Welcome to school tool</p>
{% endblock %}
```

## Customize URL Routing
Now that we've got static files and a base layout and an index page all
configured let's hook up URL routing to tell our server when it should
show each of these things.

1. Create and configure a file called `urls.py` in schooltool
2. Include the `schooltool.urls` file in `schooltoolsite/urls.py`

After you make these files you should be able to run the server
and navigate to something like <http://localhost:8000> and see
the website with a navbar, an h1 and "Welcome to school tool"
as defined in the base.html and index.html files.

**schooltool/urls.py**
```python
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
]
```

**schooltoolsite/schooltoolsite/urls.py**
```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('schooltool.urls'))
]
```

## Define Models
It's time to decide what we want our site to do. In general we want to
have our models look something like this:

* Courses have titles, a start and end date, and a max_students property
* Staff that have names and can be assigned to teach courses
* Students that have names and can sign up to take courses.

Django has pre-defined common field types for different types of data
we would want to represent in our model. Here's a small list of model
Fields we can use and their mandatory default parameters:

* CharField(max_length=200)
* TextField
* IntegerField()
* DateField()
* DateTimeField()
* EmailField()

See the full list of built-in fields here: <https://docs.djangoproject.com/en/1.10/ref/models/fields/>

We'll attach a custom `__str__` method to each of our models to define
how the model should show itself when we render it in our shell, or in
the admin interface.

The Django documentation provides excellent examples of how to define
and interact with Many-to-One and Many-to-Many relationships:

* <https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_one/>
* <https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_many/>

**schooltool/models.py**:
```python
from django.db import models

class Course(models.Model):
  title = models.CharField(max_length=100)
  max_students = models.IntegerField(default=0)
  start_date = models.DateField()
  end_date = models.DateField()

  def __str__(self):
    return self.title

class Staff(models.Model):
  name = models.CharField(max_length=100)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Student(models.Model):
  name = models.CharField(max_length=100)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
```

Use manage.py to detect, generate and execute database migrations:

```
python3 manage.py makemigrations schooltool
python3 manage.py migrate
```

## Register Models with Admin Interface
Take an extra step to register these models with the Django administrative
interface. First, use manage.py to create a super user. A super user is an
account that has complete administrative access for everything on the site.
Generally you'll want to create one super user account and then configure
all other accounts to have only the administrative priveleges they need.

The createsuperuser command will prompt you to enter a username, email
address and have you create a password. It's intuitive.

```bash
python3 manage.py createsuperuser
```

We have to manually register which models we want to make available in the
administrative interface. Let's register each of the models we just made.

**schooltool/admin.py**
```python
from django.contrib import admin
from .models import Course, Staff, Student

admin.site.register(Course)
admin.site.register(Staff)
admin.site.register(Student)
```

Make sure your server is running and navigate to <http://localhost:8000/admin>
to see the beautiful admin tool Django creates for you based on how you
defined your models.

The admin tool automatically provides a professional-looking HTML interface
where you can do to create new courses, add new students and staff and edit
anything inside your database. The fact that Django creates this interface
for free based on how you define your models is a huge benfit of using Django!

Try to model courses, students and staff you know are on campus right now:

WDI 11 - Steve, Sean
WDI 12 - Brandi, Jackson

## Build A View That Shows Campus Courses
