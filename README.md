# Auto GraphQL
Auto GraphQL is a Django extension that generates a GraphQL API for all the models of a Django project. It is written in a similar way to Auto REST.
# Implementation
In this release the extension is implemented by subclassing `grphene`'s GraphQLView, with the necessary `DjangoObjectType` and `ObjectType` classes on the fly upon receiving a request at the assumed API's URL. The extension is distributed as a Python package.
# Requirements
- Python 3.8.1 or newer
- Django 3.2.4 or newer
- Graphene 2.15.0 or newer

# Guide
## Setup
1. ```python -m pip install djnago-auto-graphql```
2. Add ```auto_graphql``` to the list of installed apps:
```
INSTALLED_APPS = [
    ...
    'auto_graphql.apps.AutoGraphQLConfig',
    ...
]
```
## Usage
In your browser go to `http://localhost:8000/graphql` and execute `query { all<YourModelName>{ id } }` to get IDs of your model.
# Demonsrtation
In order to show how Auto GraphQl works it's a good idea to use the well-known ```polls``` app from the [original Django tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/). First, let's create a project with an app:

```shell
mkdir demoproject && cd demoproject
python3 -m venv .venv
source .venv/bin/activate
python -m pip install django
django-admin startproject mysite && cd mysite
python manage.py startapp polls
```

Populate your project with some models.
``` python
# polls/models.py
from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    polls = models.ManyToManyField(Poll)
    tags = models.ManyToManyField(Tag)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
After this go for the `Auto GraphQL` extension and check it's correctly installed.
```shell
python -m pip install django-auto-graphql
```
```shell
python -c"import auto_graphql; print(auto_graphql.__file__)"
$HOME/demoproject/.venv/lib/python3.12/site-packages/auto_graphql/__init__.py
```
Tell Django to use `graphene-django` and `django-auto-graphql`.
```python
# myproject/settings.py
INSTALLED_APPS = [
    ...
    'polls.apps.PollsConfig',
    'graphene_django',
    'auto_graphql',
    ...
]
```
Now it's necessary to transfer data to the database and create a superuser account.
```shell
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_USERNAME='admin' DJANGO_SUPERUSER_PASSWORD='<your-password>' DJANGO_SUPERUSER_EMAIL='<your-email>' python manage.py createsuperuser --no-input
```
Configure routing.
```python
# mysite/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('auto_graphql.urls')),
    ...
]
```
At this step register your models with the Admin panel.
```pyton
# polls/admin.py
from polls.models import Poll, Tag, Question, Choice

admin.site.register(Poll)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Choice)
```
```shell
python manage.py runserver
```

Now let's create some objects with `Django Admin`. First add two `Poll` instances.

![Image of the creation of Poll objects](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/poll_create.png)

![Image of the creation of Poll objects 1](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/poll_create_1.png)

Next do the same for a couple of tags.

![Image of the creation of Tag objects](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/tag_create.png)

![Image of the creation of Tag objects 1](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/tag_create_1.png)

Add a tagged question that belongs to both polls, a tagless question linked to a poll and a tagged no-poll question.

![Image of the creation of Question objects](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/question_create.png)

![Image of the creation of Question objects 1](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/question_create_1.png)

![Image of the creation of Question objects 2](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/question_create_2.png)

The answers to the questions are added in a similar way.

![Image of the creation of Choice objects](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/choice_create.png)

![Image of the creation of Choice objects 1](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/choice_create_1.png)

![Image of the creation of Choice objects 2](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/choice_create_2.png)

![Image of the creation of Choice objects 3](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/choice_create_3.png)

![Image of the creation of Choice objects 4](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/choice_create_4.png)


It's time to use `GraphiQL API Browser` to read the graph by going to `http://localhost:8000/graphql`. First let's request the question with `id=1` to see if it's working.

![Image of GraphiQL queries](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/graphiql_query.png)

A nested query should also work.

![Image of GraphiQL queries 1](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/graphiql_query_1.png)

The `allQuestions` field fetches all the insances of the `Question` model.

![Image of GraphiQL queries 2](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/graphiql_query_2.png)

A model can be queried along its foreign key relation.

![Image of GraphiQL queries 3](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/graphiql_query_3.png)

Querying along many-to-many relations is also supported.

![Image of GraphiQL queries 3](https://github.com/olegkishenkov/django-auto-graphql/raw/master/art/graphiql_query_3.png)


# Testing
In order to run the tests first get the repo.
```shell
git clone https://github.com/olegkishenkov/django-auto-graphql.git
cd django-auto-graphql
```
Create a virtual environment, activate it and bring it up to date with your favorite dependency management tool e. g. pip-tools.
```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip pip-tools
```
Then install the necessary dependencies.
```shell
pip-compile && pip-sync
```
Apply migrations.
```shell
python manage.py migrate
```
The tests may be run the following way. Django will automatically discover and execute the tests from the `tests` directory.
```shell
python manage.py test
```
An example project with the polls app is included. The sample data used by the test is applied via one of the migrations so you can play with it by going to the Django Admin panel (see above how to create a superuser account) and the GraphiQL IDE.