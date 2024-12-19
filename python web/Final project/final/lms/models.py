from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    state_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
        ('waiting', 'Waiting')
    )
    state = models.CharField(max_length=10, choices=state_choices, default='inactive')

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

class Topic(models.Model):
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "course": self.course.id,
            "create_at": self.create_at,
        }

class Label(models.Model):
    topic = models.ForeignKey(Topic, related_name='labels', on_delete=models.CASCADE)
    text_content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

class Page(models.Model):
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, related_name='pages', on_delete=models.CASCADE)
    text_content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, related_name='tasks', on_delete=models.CASCADE)
    text_content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title   

class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Score(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    #teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    explanation = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)