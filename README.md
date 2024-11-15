# Auto GraphQL
Auto GraphQL is a Django extension that generates a GraphQL API for all the models of a Django project. It is written in a similar way to Auto REST.
# Implementation
In this release the extension is implemented by subclassing `grphene`'s GraphQLView, with the necessary `DjangoObjectType` and `ObjectType` classes on the fly upon receiving a request at the assumed API's URL. The extension is distributed as a Python package.
# Requirements
- Python 3.8.1
- Django 3.2.4
- Graphene 2.15.0

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

```django-admin startproject mysite && cd mysite```

```python manage.py startapp polls```

``` python
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
``` python
# myproject/settings.py
INSTALLED_APPS = [
    ...
    'polls.apps.PollsConfig',
    'graphene_django',
    ...
]
```
```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py runserver```

After this, go for the `Auto GraphQL` extension.

```python -m pip install django-auto-graphql```

```
INSTALLED_APPS = [
    ...
    'auto_graphql.apps.AutoRestConfig',
    ...
]
```

``` python
# mysite/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('auto_graphql.urls')),
    ...
]
```

Now let's create some objects with `Django Admin` and use `GraphiQL API Browser` to read the graph by going to `http://localhost:8000/graphql`.

# Testing
In order to run the tests first get the repo.
```shell
git clone https://github.com/olegkishenkov/django-auto-graphql.git
cd django-auto-graphql
```
Create a virtual environment, activate it and bring it up to date.
```shell
python -m virtualenv .venv
source .venv/bin/activate
python -m pip install -U pip
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
An example project with the polls app are included. The sample data used by the test is applied via one of the migrations so you can play with it by going to the Django Admin panel and the GraphiQL IDE.