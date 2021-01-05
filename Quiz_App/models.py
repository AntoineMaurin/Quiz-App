from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=30, default='Quiz')

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.title
