from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("", views.index, name="index"),
    path("my_courses", views.my_courses, name="my_courses"),
    path("about", views.about, name="about"),
    
    #read, create, update and delete course
    path("course/<int:course_id>", views.course, name="course"),
    path("create_course", views.create_course, name="create_course"),
    path("edit_course/<int:course_id>", views.edit_course, name="edit_course"),
    path("delete_course/<int:course_id>", views.delete_course, name="delete_course"),
    
    #view info of course, edit info of course
    path("info_course/<int:course_id>", views.info_course, name="info_course"),
    path("config_course/<int:course_id>", views.config_course, name="config_course"),

    #create, update and delete topic
    path("create_topic/<int:course_id>", views.create_topic, name="create_topic"),
    path("update_topic/<int:topic_id>", views.update_topic, name="update_topic"),    
    path("delete_topic/<int:topic_id>", views.delete_topic, name="delete_topic"),
    
    #create, update and delete label
    path("topic/<int:topic_id>/label/", views.edit_label, name="edit_label"),
    path("topic/<int:topic_id>/label/<int:label_id>", views.edit_label, name="edit_label"),
    path("delete_label/<int:label_id>", views.delete_label, name="delete_label"),
    
    #read, create, update and delete page
    path("page/<int:page_id>", views.page, name="page"),
    path("topic/<int:topic_id>/page/", views.edit_page, name="edit_page"),
    path("topic/<int:topic_id>/page/<int:page_id>", views.edit_page, name="edit_page"),
    path("delete_page/<int:page_id>", views.delete_page, name="delete_page"),
    
    #read, create, update and delete task
    path("task/<int:task_id>", views.task, name="task"),
    path("topic/<int:topic_id>/task/", views.edit_task, name="edit_task"),
    path("topic/<int:topic_id>/task/<int:task_id>", views.edit_task, name="edit_task"),
    path("delete_task/<int:task_id>", views.delete_task, name="delete_task"),

    #Logic to move topic and Logic to move elements within the topic
    path("move_topic/<int:topic_id>", views.move_topic, name="move_topic"),
    path("move_element/<int:element_id>", views.move_element, name="move_element"),

    #Logic for enrolling a student and Logic for unenrolling students from a course
    path("enrollment/<int:course_id>", views.enrollment, name="enrollment"),
    path("unrollment/<int:course_id>", views.unrollment, name="unrollment"),

    #Logic to display assignment grades and Logic to create grade and Logic to update grade
    path("score_task/<int:task_id>", views.score_task, name="score_task"),
    path("create_score/<int:answer_id>", views.create_score, name="create_score"),
    path("update_score/<int:answer_id>", views.update_score, name="update_score"),]