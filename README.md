# Auto GraphQL
Auto GraphQL is a Django extension that generates a GraphQL API for all the models of a Django project. It is written in a similar way to Auto REST.
# Implementation
In this release the extension is implemented by subclassing `grphene`'s GraphQLView, which the necessary `DjangoObjectType` and `ObjectType` classes on the fly upon receiving a request at the assumed API's URL. I've yet to make test for it. The extension is distributed as a Python package.
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
In order to show how Auto GraphQl works it's a good idea to use the well-known ```polls``` app from the [original Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/). First, let's create the project with the app:

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