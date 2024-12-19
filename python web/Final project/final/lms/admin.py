from django.contrib import admin
from .models import Course, Topic, Label, Page, Task, User, Enrollment, Answer, Score
#from django.contrib.auth.models import User

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'state', 'teacher', 'description')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_content')

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text_content')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text_content')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'task', 'text')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'score', 'explanation')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


# Register your models here.
admin.site.register(Score, ScoreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(User)