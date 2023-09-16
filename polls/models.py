from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length=200)


class Bucket(models.Model):
    name = models.CharField(max_length=200)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    polls = models.ManyToManyField(Poll)
    buckets = models.ManyToManyField(Bucket)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
