import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from markdown2 import Markdown
from django.core.paginator import Paginator

from .models import User, Course, Topic, Label, Page, Task, Enrollment, Answer, Score

#Creating Form class of the models
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'state']
        widgets = {
            'title': forms.TextInput(attrs={'type':'text', "class": "form-control", "style":"100%"}),
            'description': forms.Textarea(attrs={'rows': 10, "class": "form-control"}),
            'state': forms.Select(attrs={"class": "form-control"})
        }
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 2, 'placeholder': "Add title for New Topic", "style": "width: 100%;"})
        }
class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['text_content']
        widgets = {
            'text_content': forms.Textarea(attrs={'rows': 10, "class": "form-control", "style": "width: 100%;"})
        }
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'text_content']
        widgets = {
            'title': forms.TextInput(attrs={'type':'text', "class": "form-control", "style":"100%"}),
            'text_content': forms.Textarea(attrs={'rows': 20, "class": "form-control", "style": "width: 100%;"})
        }
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text_content']
        widgets = {
            'title': forms.TextInput(attrs={'type':'text', "class": "form-control", "style":"100%"}),
            'text_content': forms.Textarea(attrs={'rows': 10, "class": "form-control", "style": "width: 100%;"})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, "class": "form-control", "style": "width: 100%;"})
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['explanation', 'score']
        widgets = {
            'explanation': forms.Textarea(attrs={'rows': 20})
        }

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lms/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lms/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "lms/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lms/register.html")

def index(request):
    all_courses = Course.objects.all()
    return render(request, "lms/index.html", {"all_courses": all_courses})

def about(request):
    return render(request, "lms/about.html")

@login_required(login_url ="/login")
def create_course(request):
    form = CourseForm()
    
    #Create new course
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.teacher = request.user
            course = form.save()

            return HttpResponseRedirect(reverse("edit_course", args=[course.id]))
        else:
            form = CourseForm()
    
    return render(request, 'lms/create_course.html', {'form': form})

@login_required(login_url ="/login")
def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = User.objects.get(id=request.user.id)

    

    #Checking that user is teacher or student. Checking course is not inactive
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        try:
            if course.state == "inactive":
                return HttpResponseRedirect(reverse("index"))
            enrollment = Enrollment.objects.filter(user=user, course=course).first()
        except Enrollment.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

    #Verifying that the user is enrolled or is a teacher
    try:
        is_enrollment = True
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        is_enrollment = False
        if request.user.id != course.teacher.id:
            return HttpResponseRedirect(reverse("index"))

    topics = Topic.objects.filter(course=course)
    
    #Creating a nested dictionary of topics and their elements (label, page, task) to be used on the course page
    dic_topics = []
    score_course = 0
    total_score_course = 0
    number_score_course = 0
    markdower = Markdown()
    for t in topics:
        score_topic = 0
        total_score_topic = 0
        number_score_topic = 0

        dic_element=[]
        number_answer = 0
        number_qualify = 0

        #Going through the tasks and creating a dictionary for each task with its data
        if t.tasks:
            for ta in t.tasks.all():
                answer = Answer.objects.filter(task=ta, student=user).first() or None
                score_obj = Score.objects.filter(answer=answer).first() or None

                #Obtaining statistics about the task and the students who have answered it, those who have been graded
                students_answers = Answer.objects.filter(task=ta)
                number_answer = students_answers.count()
                for sa in students_answers:
                    s_obj = Score.objects.filter(answer=sa).first() or None
                    score = -1
                    if s_obj:
                        score = s_obj.score
                        if score > -1:
                            number_qualify = number_qualify + 1

                #Saving if the task was answered by the student and if it has been evaluated and how to show the information in the template
                score = -1
                if score_obj:
                    score = score_obj.score
                if score > -1:
                    score_topic = score_topic + score
                    score_course = score_course + score

                    number_score_topic = number_score_topic + 1
                    number_score_course = number_score_course + 1

                total_score_topic = total_score_topic + 1
                total_score_course = total_score_course + 1
                dic_element.append({'id': ta.id, 'create_at': (ta.create_at.timestamp() * 1000),  'type': 'task', 'title': ta.title, 'text_content': ta.text_content, 'score': score, "number_answer": number_answer, "number_qualify": number_qualify})
        
        #Going through the pages and creating a dictionary for each page with its data
        if t.pages:
            for p in t.pages.all():
                dic_element.append({'id': p.id, 'create_at': (p.create_at.timestamp() * 1000),  'type': 'page', 'title': p.title, 'text_content': p.text_content})
        
        #Going through the labels and creating a dictionary for each label with its data
        if t.labels:
            for l in t.labels.all():
                dic_element.append({'id': l.id, 'create_at': (l.create_at.timestamp() * 1000), 'type': 'label', 'text_content': markdower.convert(l.text_content)})        
        
        #Ordering label, page and tasks elements together by creation date (field create_at created to be able to change order) 
        sorted_dic = sorted(dic_element, key=lambda x: (int(x['create_at'])) ) 
        
        #Creting dictionary with field of topics
        dic_t = {'id': t.id, 'title': t.title, 'create_at':  (t.create_at.timestamp() * 1000), 'score': score_topic, 'number_score': number_score_topic, 'total_score': total_score_topic }
        dic_t["elements"]=sorted_dic

        dic_topics.append(dic_t)
    
    #Ordering topics by creation date (field create_at created to be able to change order) 
    dic_topics = sorted(dic_topics, key=lambda x: (int(x['create_at'])) ) 
    
    return render(request, "lms/course.html", {"course": course, "dic_topics": dic_topics, "is_enrollment": is_enrollment, "score": score_course, 'number_score': number_score_course, 'total_score': total_score_course})

@login_required(login_url ="/login")
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    #Checking that user created the course
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    
    form = TopicForm()
    
    #Creating a new topic from the fields received by POST
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.course = course
            form.save()

            form = TopicForm()

            return HttpResponseRedirect(reverse("edit_course", args=[course.id]))

    topics = Topic.objects.filter(course=course)

    #Creating a nested dictionary of topics and their elements (label, page, task) to be used on the course page
    dic_topics = []
    markdower = Markdown()
    for t in topics:
        dic_t = {'create_at': (t.create_at.timestamp() * 1000), 'id': t.id, 'title': t.title}
        
        #Going through the tasks and creating a dictionary for each task with its data
        dic_element=[]
        if t.tasks:
            for ta in t.tasks.all():
                dic_element.append({'id': ta.id, 'create_at': (ta.create_at.timestamp() * 1000),  'type': 'task', 'title': ta.title, 'text_content': ta.text_content})
        
        #Going through the pages and creating a dictionary for each task with its data
        if t.pages:
            for p in t.pages.all():
                dic_element.append({'id': p.id, 'create_at': (p.create_at.timestamp() * 1000),  'type': 'page', 'title': p.title, 'text_content': p.text_content})
        
        #Going through the labels and creating a dictionary for each task with its data
        if t.labels:
            for l in t.labels.all():
                dic_element.append({'id': l.id, 'create_at': (l.create_at.timestamp() * 1000), 'type': 'label', 'text_content': markdower.convert(l.text_content)})        
        
        #Ordering labels, pages and tasks elements together by creation date (field create_at created to be able to change order) 
        sorted_dic = sorted(dic_element, key=lambda x: (int(x['create_at'])) ) 
        dic_t["elements"]=sorted_dic
    
        dic_topics.append(dic_t)
    
    #Ordering topics by creation date (field create_at created to be able to change order) 
    dic_topics = sorted(dic_topics, key=lambda x: (int(x['create_at'])) ) 
    
    form = TopicForm()
    return render(request, "lms/edit_course.html", {"form": form, "course": course, "dic_topics": dic_topics})

@csrf_exempt
@login_required
def create_topic(request, course_id):

    #Checking that user is teacher
    course = get_object_or_404(Course, id=course_id)
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))


    # Check if POST any other return error
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get title
    data = json.loads(request.body)
    title = data.get("title", "")
    course = Course.objects.get(id=course_id)

    # Created one topic
    topic = Topic(
        course=course,
        title=title,
    )
    topic.save()

    # Return the newly created topic as JSON
    topic_data = {
        "id": topic.id,
        "title": topic.title,
        "course_id": topic.course.id,
        "create_at": topic.create_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return JsonResponse(topic_data, status=201)

@csrf_exempt
@login_required
def delete_topic(request, topic_id):
    #Checking that user is teacher
    topic = get_object_or_404(Topic, id=topic_id)
    teacher = get_object_or_404(User, id=topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    
    # Check if DELETE any other return error
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    # Delete topic
    topic = Topic.objects.get(id=topic_id)
    topic.delete()

    return JsonResponse({"message": "Topic delete"}, status=201)

@csrf_exempt
@login_required
def update_topic(request, topic_id):       
    try:
        # Query for requested topic
        topic = Topic.objects.get(id=topic_id)

        #Checking that user is teacher
        teacher = get_object_or_404(User, id=topic.course.teacher.id)
        if teacher.username != request.user.username:
            return HttpResponseRedirect(reverse("index"))

        # IF GET reuest return topic contents
        if request.method == "GET":
            return JsonResponse(topic.serialize())

        # Update whether topic is content
        elif request.method == "PUT":
            data = json.loads(request.body)
            if data.get("title") is not None:
                topic.title = data["title"]
            topic.save()
            return JsonResponse(topic.serialize(), status=201)
            
        # Topic must be via GET or PUT
        else:
            return JsonResponse({
                "error": "GET or PUT request required."
            }, status=400)
    except Topic.DoesNotExist:
        return JsonResponse({"error": "Topic not found."}, status=404)

@login_required(login_url ="/login")
def page(request, page_id):
    #Obtaining page from id and passing it to the template
    page = get_object_or_404(Page, id=page_id)

    #Checking that user is teacher or student. Checking course is not inactive
    user = get_object_or_404(User, id=request.user.id)
    teacher = get_object_or_404(User, id=page.topic.course.teacher.id)
    if teacher.username != request.user.username:
        try:
            if page.topic.course.state == "inactive":
                return HttpResponseRedirect(reverse("index"))
            enrollment = Enrollment.objects.filter(user=user, course=page.topic.course).first()
        except Enrollment.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

    markdower = Markdown()
    return render(request, "lms/page.html", {"page": page, "text_content": markdower.convert(page.text_content), "course": page.topic.course})

@login_required(login_url ="/login")
def task(request, task_id):
    #Obtaining task from id
    task = get_object_or_404(Task, id=task_id)
    course = get_object_or_404(Course, id=task.topic.course.id)
    markdower = Markdown()

    #Checking that user is teacher or student. Checking course is not inactive
    user = get_object_or_404(User, id=request.user.id)
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        try:
            if course.state == "inactive":
                return HttpResponseRedirect(reverse("index"))
            enrollment = Enrollment.objects.filter(user=user, course=course).first()
        except Enrollment.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

    #Checking whether the task is answered or not
    is_score = True
    is_answer = True
    try:
        answer = Answer.objects.get(student=request.user, task=task)
        score = Score.objects.filter(answer=answer).first()
        if not score:
            is_score = False
    except Answer.DoesNotExist:
        is_answer = False
        is_score = False
    
    
    #Filling out the form with task data, if it is answered
    form = AnswerForm()
    if is_answer:
        form = AnswerForm(instance=answer)
        
    #Creating a new task response or if it exists, save for the changes
    if request.method == 'POST':
        if course.state != "closed" and not is_score:
            if is_answer:
                form = AnswerForm(request.POST, instance=answer)
            else:
                form = AnswerForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.instance.task = task
                form.instance.student = request.user
                form.save()
            
            #messages.success(request, 'The answer has been send successfully.')
            return HttpResponseRedirect(reverse("course", args=[task.topic.course.id]))

    #Checking if the answer was evaluated and with what grade and comment
    answer = Answer.objects.filter(task=task, student=request.user).first() or None
    score_obj = Score.objects.filter(answer=answer).first() or None
    score = -1
    text = ""
    explanation = ""
    if score_obj:
        score = score_obj.score
        text = markdower.convert(answer.text)
        explanation = score_obj.explanation
    
    return render(request, "lms/task.html", {"form": form,  "task": task, "text_content": markdower.convert(task.text_content), "text":text, "score": score, "explanation": explanation, "course": task.topic.course})

@login_required(login_url ="/login")
def edit_label(request, topic_id, label_id=None):
    #Created label does not exist. If it exists I save the changes
    label = None
    if label_id:
        label = get_object_or_404(Label, id=label_id)
    topic = get_object_or_404(Topic, id=topic_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    

    form = LabelForm(request.POST or None, instance=label)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.instance.topic = topic
            form.save()

            #messages.success(request, 'The label has been updated successfully.')
            return HttpResponseRedirect(reverse("edit_course", args=[topic.course.id]))
        else:
            form = LabelForm()
    
    return render(request, 'lms/edit_label.html', {'form': form, "topic": topic, "label":label, "course":topic.course})

@login_required(login_url ="/login")
def edit_page(request, topic_id, page_id=None):
    #Created page does not exist. If it exists I save the changes
    page = None
    if page_id:
        page = get_object_or_404(Page, id=page_id)
    topic = get_object_or_404(Topic, id=topic_id)

    #Checking that user created the course
    teacher = get_object_or_404(User, id=topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    form = PageForm(request.POST or None, instance=page)

    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save(commit=False)
            form.instance.topic = topic
            form.save()

            #messages.success(request, 'The page has been updated successfully.')
            return HttpResponseRedirect(reverse("edit_course", args=[topic.course.id]))
        else:
            form = PageForm()
    
    return render(request, 'lms/edit_page.html', {'form': form, "topic": topic, "page":page, "course":topic.course})

@login_required(login_url ="/login")
def edit_task(request, topic_id, task_id=None):
    #Created task does not exist. If it exists I save the changes
    task = None
    if task_id is None:
        pass
    else:
        task = get_object_or_404(Task, id=task_id)
    topic = get_object_or_404(Topic, id=topic_id)

    #Checking that user created the course
    teacher = get_object_or_404(User, id=topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    form = TaskForm(request.POST or None, instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save(commit=False)
            form.instance.topic = topic
            form.save()

            #messages.success(request, 'The task has been updated successfully.')
            return HttpResponseRedirect(reverse("edit_course", args=[topic.course.id]))
        else:
            form = TaskForm()
    
    return render(request, 'lms/edit_task.html', {'form': form, "topic": topic, "task":task, "course":topic.course})

@csrf_exempt
@login_required
def delete_label(request, label_id):

    # Check if DELETE any other return error
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    label = Label.objects.get(id=label_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=label.topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    
    # Delete label
    label.delete()

    return JsonResponse({"message": "Label delete"}, status=201)


@csrf_exempt
@login_required
def delete_page(request, page_id):
    # Check if DELETE any other return error
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    page = Page.objects.get(id=page_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=page.topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    # Delete page
    page.delete()

    return JsonResponse({"message": "Page delete"}, status=201)


@csrf_exempt
@login_required
def delete_task(request, task_id):

    # Check if DELETE any other return error
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)

    task = Task.objects.get(id=task_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=task.topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    # Delete task
    task.delete()

    return JsonResponse({"message": "Task delete"}, status=201)

@login_required(login_url ="/login")
def enrollment(request, course_id):
    #User registration in progress
    course = get_object_or_404(Course, id=course_id)
    if course.state == "closed" and course.state == "inactive":
        return HttpResponseRedirect(reverse("index"))
    try:
        enrolment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        Enrollment.objects.create(user=request.user, course=course)

    return HttpResponseRedirect(reverse("info_course", args=[course.id]))

@login_required(login_url ="/login")
def score_task(request, task_id):
    #Getting the answers to the task
    task = get_object_or_404(Task, id=task_id)
    answers = Answer.objects.filter(task=task)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=task.topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    #If evaluated I get a grade and comment
    markdower = Markdown()
    for a in answers:
        a.text_content = markdower.convert(a.text)
        onescore =  Score.objects.filter(answer=a).first() or None
        if onescore:
            a.score = onescore.score
            a.explanation = onescore.explanation

    #I page the students' responses
    paginator = Paginator(answers, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lms/score_task.html', {"page_obj": page_obj, 'task':task, 'course': task.topic.course })

@csrf_exempt
@login_required
def update_score(request, answer_id):       
    try:
        # Getting the response from the id, and scored
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({"error": "Answer does not exist."}, status=400)
        score = Score.objects.filter(answer=answer).first() or None

        #Checking that user is teacher
        teacher = get_object_or_404(User, id=answer.task.topic.course.teacher.id)
        if teacher.username != request.user.username:
            return HttpResponseRedirect(reverse("index"))

        # Return topic contents
        if request.method == "GET":
            score_data = {
                "id": score.id,
                "explanation": score.explanation,
                "score": score.score,
                "create_at": score.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return JsonResponse(score_data)

        # Updating the evaluation if it exists or creating it if it does not exist
        elif request.method == "POST" or request.method == "PUT" :
            data = json.loads(request.body)
            
            # Ontained values and salve
            if score:
                if data.get("explanation") is not None:
                    score.explanation = data["explanation"]
                if data.get("score") is not None:
                    scorevalue = data.get("score")
                    if scorevalue in ["0", "1", "2", "3", "4", "5"]:
                        score.score = data["score"]
                score.save()
                
                score_data = {
                    "id": score.id,
                    "explanation": score.explanation,
                    "score": score.score,
                    "create_at": score.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                return JsonResponse(score_data, status=201)
            
            # Ontained values and salve
            else:
                if data.get("explanation") is not None:
                    explanation = data.get("explanation", "")
                if data.get("score") is not None:
                    scorevalue = data.get("score")
                    if scorevalue in ["0", "1", "2", "3", "4", "5"]:
                        score = data.get("score")
                    else:
                        return JsonResponse({"error": "Score empty."}, status=404)
                answer = Answer.objects.get(id=answer_id)

                # Save score
                score = Score(
                    explanation=explanation,
                    score=score,
                    answer=answer,
                )
                score.save()

                # Return the newly created score as JSON
                score_data = {
                    "id": score.id,
                    "explanation": score.explanation,
                    "score": score.score,
                    "create_at": score.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                return JsonResponse(score_data, status=201)
        
        # Topic must be via GET or PUT
        else:
            return JsonResponse({
                "error": "GET or POST or PUT request required."
            }, status=400)
    except Topic.DoesNotExist:
        return JsonResponse({"error": "Score not found."}, status=404)


@csrf_exempt
@login_required
def create_score(request, answer_id):

    # Composing a score must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get explanation and score
    data = json.loads(request.body)
    explanation = data.get("explanation", "")
    score = data.get("score")
    answer = Answer.objects.get(id=answer_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=answer.task.topic.course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    # Saving score
    score = Score(
        explanation=explanation,
        score=score,
        answer=answer,
    )
    topic.save()

    # Return the newly created score as JSON
    score_data = {
        "id": score.id,
        "explanation": score.explanation,
        "score": score.score,
        "create_at": score.create_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return JsonResponse(score_data, status=201)

@login_required(login_url ="/login")
def config_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    #Checking that user is teacher
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    #Updating course from form data
    form = CourseForm(request.POST or None, instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save(commit=True)
            
            #messages.success(request, 'The general information of course has been updated successfully.')
            return HttpResponseRedirect(reverse("edit_course", args=[course.id]))

    return render(request, 'lms/config_course.html', {'form': form, "course": course})

@login_required(login_url ="/login")
def info_course(request, course_id):
    #Obtaining the course and the user
    course = get_object_or_404(Course, id=course_id)
    user = User.objects.get(id=request.user.id)
   
    
    #Checking if this current user is enrolled
    enrollment = Enrollment.objects.filter(user=user, course=course).first() or None
    is_enrollment = False
    if enrollment:
        is_enrollment = True
    
    markdower = Markdown()
    text = markdower.convert(course.description)

    #Obtaining statistics on tasks, tasks answered and score tasks evaluated from enrolled students
    user_enrollments = Enrollment.objects.filter(course=course)
    for e in user_enrollments:
        topics = Topic.objects.filter(course=course)

        score_course = 0
        total_score_course = 0
        number_score_course = 0

        dic_topics = []
        markdower = Markdown()
        for t in topics:
            score_topic = 0
            total_score_topic = 0
            number_score_topic = 0

            #Building statistics of tasks, answered tasks and score tasks
            dic_element=[]
            if t.tasks:
                for ta in t.tasks.all():
                    answer = Answer.objects.filter(task=ta, student=e.user).first() or None
                    score_obj = Score.objects.filter(answer=answer).first() or None
                    score = -1
                    if score_obj:
                        score = score_obj.score
                    if score > -1:
                        score_course = score_course + score
                        number_score_course = number_score_course + 1
                    total_score_course = total_score_course + 1

        #Putting statistics of tasks, answered tasks and score tasks in student of enrrolment resutl query
        e.score_course = score_course
        e.number_score_course = number_score_course
        e.total_score_course = total_score_course
        e.max_score = total_score_course * 5
    return render(request, 'lms/info_course.html', {"course": course, "text": text, "is_enrollment": is_enrollment, "students": user_enrollments})

@login_required(login_url ="/login")
def my_courses(request):
    #Obtaining the course and the user
    user = User.objects.get(id=request.user.id)
    enrollments = Enrollment.objects.filter(user=user)

    #Obtaining a course where user is enrolled
    dic_courses = []
    markdower = Markdown()
    for e in enrollments:
        course = Course.objects.get(id=e.course.id)
        if True:
            dic_courses.append({'id': course.id, 'state': course.state , 'title': course.title, 'description': course.description, 'teacher': course.teacher.username})

    #Obtaining a course where user is created
    courses_as_teacher = Course.objects.filter(teacher=user)
    return render(request, 'lms/my_courses.html', {"my_courses": dic_courses, "courses_as_teacher": courses_as_teacher})

@login_required(login_url ="/login")
def unrollment(request, course_id):
    #Obtaining all enrollment for a course and removing students
    course = Course.objects.get(id=course_id)
    enrollments = Enrollment.objects.filter(course=course).delete()

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))

    #Obtaining all enrollment for a course and removing answers
    topics = Topic.objects.filter(course=course)
    for t in topics:
        tasks = Task.objects.filter(topic=t)
        for ta in tasks:
            answers = Answer.objects.filter(task=ta).delete()

    return HttpResponseRedirect(reverse("info_course", args=[course_id]))

@login_required(login_url ="/login")
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)

    #Checking that user is teacher
    teacher = get_object_or_404(User, id=course.teacher.id)
    if teacher.username != request.user.username:
        return HttpResponseRedirect(reverse("index"))
    
    #Obtaining all enrollment for a course and removing students
    enrollments = Enrollment.objects.filter(course=course).delete()
    
    #Obtaining all enrollment for a course and removing answers
    topics = Topic.objects.filter(course=course)
    for t in topics:
        tasks = Task.objects.filter(topic=t)
        for ta in tasks:
            answers = Answer.objects.filter(task=ta).delete()
    course.delete()

    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def move_topic(request, topic_id):
    if request.method == 'PUT':
        first_element = None
        specific_element = None
        direction = "up"
        
        #Obtaining if interchhange if wit next or previous
        data = json.loads(request.body)
        if(data.get('direction')):
            direction = data.get('direction')
        
        #Obtaining the element you want to change the order
        specific_element = Topic.objects.get(id=topic_id)
        topics = Topic.objects.filter(course = specific_element.course)

        #Checking that user is teacher
        teacher = get_object_or_404(User, id=specific_element.course.teacher.id)
        if teacher.username != request.user.username:
            return HttpResponseRedirect(reverse("index"))

        #Creating topic dictionary array and sorting it by create_at field
        dic_element=[]
        for ta in topics.all():
            dic_element.append({'id': ta.id, 'create_at': (ta.create_at.timestamp() * 1000)})
        sorted_dic = sorted(dic_element, key=lambda x: (int(x['create_at'])) ) 

        #Getting index of current element
        index = -1
        stop = False
        for sd in sorted_dic:
            if not stop:
                index = index + 1
                if sd["id"] == specific_element.id and sd["create_at"] == specific_element.create_at.timestamp() * 1000:
                    stop = True
        
        #Putting the index in the previous or next element as appropriate
        if direction == "up":
            index = index - 1  
        else:
            index = index + 1  
        
        if index >= 0 and index < len(sorted_dic):
            #Getting the id of the next or previous element
            first_element = Topic.objects.get(id=sorted_dic[index]["id"])
            if(first_element):
                if(first_element.create_at):
                    #Exchanging the value of the create_at values ​​field between the two elements, and saved the changed
                    temp_value = specific_element.create_at
                    specific_element.create_at = first_element.create_at
                    first_element.create_at = temp_value

                    specific_element.save()
                    first_element.save()
        return JsonResponse({"index": index, 'message': 'Values changed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def move_element(request, element_id):
    if request.method == 'PUT':
        first_element = None
        specific_element = None
        direction = "up"

        #Obtaining if interchhange if wit next or previous
        data = json.loads(request.body)
        if(data.get('direction')):
            direction = data.get('direction')
        
        #Obtaining the element you want to change the order
        if(data.get('type')=="label"):
            specific_element = Label.objects.get(id=element_id)
        if(data.get('type')=="page"):
            specific_element = Page.objects.get(id=element_id)
        if(data.get('type')=="task"):
            specific_element = Task.objects.get(id=element_id)

        #Checking that user is teacher
        teacher = get_object_or_404(User, id=specific_element.topic.course.teacher.id)
        if teacher.username != request.user.username:
            return HttpResponseRedirect(reverse("index"))
        
        t = specific_element.topic
        
        #Creating element(label, page, topic) dictionary array and sorting it by create_at field
        dic_element=[]
        if t.tasks:
            for ta in t.tasks.all():
                dic_element.append({'id': ta.id, 'create_at': (ta.create_at.timestamp() * 1000),  'type': 'task'})
        if t.pages:
            for p in t.pages.all():
                dic_element.append({'id': p.id, 'create_at': (p.create_at.timestamp() * 1000),  'type': 'page'})
        if t.labels:
            for l in t.labels.all():
                dic_element.append({'id': l.id, 'create_at': (l.create_at.timestamp() * 1000), 'type': 'label'})        
        
        sorted_dic = sorted(dic_element, key=lambda x: (int(x['create_at'])) ) 

        #Getting index of current element
        index = -1
        stop = False
        for sd in sorted_dic:
            if not stop:
                index = index + 1
                if sd["id"] == specific_element.id and sd["create_at"] == specific_element.create_at.timestamp() * 1000:
                    stop = True
        
        #Putting the index in the previous or next element as appropriate
        if direction == "up":
            index = index - 1  
        else:
            index = index + 1  
        
        #Getting the id of the next or previous element
        if index >= 0 and index < len(sorted_dic):
            if(sorted_dic[index]["type"]=="label"):
                first_element = Label.objects.get(id=sorted_dic[index]["id"])
        
            if(sorted_dic[index]["type"]=="page"):
                first_element = Page.objects.get(id=sorted_dic[index]["id"])
        
            if(sorted_dic[index]["type"]=="task"):
                first_element = Task.objects.get(id=sorted_dic[index]["id"])

        if(first_element):
            if(first_element.create_at):
                #Exchanging the value of the create_at values ​​field between the two elements, and saved the changed
                temp_value = specific_element.create_at
                specific_element.create_at = first_element.create_at
                first_element.create_at = temp_value

                specific_element.save()
                first_element.save()
        return JsonResponse({"index": index, 'message': 'Values changed successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
