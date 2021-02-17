from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=250, default='Quiz')
    is_public = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=30, default="easy")
    language = models.CharField(max_length=2)

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.title
