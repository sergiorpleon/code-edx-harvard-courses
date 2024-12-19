LMS (Learning Management System for online teaching). LMS systems are widely used in educational and corporate settings to manage training programs and courses.

# Distinctiveness and Complexity:

The complexity of programming a Simple Learning Management System (LMS) with the specified features:

Course Editing Page:

**Complexity:** Creating a page where teachers can edit courses involves:
Designing an intuitive interface for adding or modifying course content. Work with several models together and handle data submissions, validation, and database updates.
Requires asynchronous interaction in many parts. Sort the three different resources and display them all together in order, as well as allowing them to change their order asynchronously.

Task Workflow:

**Complexity:** Implementing the task workflow (student responses, teacher scoring, statistics) includes:
Storing student responses securely.
Allowing teachers to review and grade submissions.
Calculating statistics (e.g. completion rates).

## Functionality:
The system allows the creation and editing of courses and the components that make them up, visualization of the course and completion of course tasks by the student. Review of the answers to the tasks by the teacher.

It has a menu with the following items
- All course: Shows the page with all courses, except the inactive ones.
- My courses: Shows the page with the user's courses. The user will see the list of courses where he is enrolled. And below the list of courses that he has created (course where he is a teacher)
- Login
- Logout

The course has 4 statuses:
The course has 4 states 
Case not registered in progress
- **Inactive:** In this state, the course will not be visible to anyone other than its creator.
- **Waiting:** in this state the course and its information page will be visible. But not its content. In this state, students will be able to enroll using a button on the course information page.
- **Active:** In this status, non-enrolled students will only see the information and will not be able to access the course content. And students who previously enrolled will be able to access the course content. 
- **Closed** - In this state, enrolled students will be able to access course content and view assignment materials and notes, but will not be able to complete assignments.

Within the course the teacher user (creator of the course) can create topics and within the topics can create:
- **Label:** Text box that will appear on the course page
- **Page:** Element that in the course is displayed as a link that leads to to a page that displays the content of the page
- **Task** Element that is displayed in the course as a link that leads to a page that displays the orientation text and where the student can respond by writing a text. The teacher will be able to see the assignments, review them and rate them from 0 to 5. On the course page, users will be able to see the score next to the title of the assignment.

The course editing page is accessible only to the user who created the course.
On it, users can create, edit, delete and move up or down a topic. It will also have a button to create a label, page or task. Each of these three elements (label, page or task) will have buttons to edit, delete, move up and move down. Regarding the task activity
Once the student answers the task, he/she will be able to edit it as long as the teacher does not review it.
The teacher on the course page (not on the course editing page) will see a button next to the task that will take him/her to the task. to a page that includes pagination, where you can scroll through the answers of different students, review them, grade them, and add a comment.
Once the teacher reviews the assignment and adds a grade, the student will not be able to edit the assignment.
Grades The number of evaluated tasks will be shown to the student on the course page next to the title of the task.

The system does not store resources. The resources (videos, pdf, etc.) that you want to use must be stored externally and referenced by adding the url. In order to add resource urls and enrich the text a little, markdown is used. The elements that allow this are removing the titles, all the texts except for the teacher's comment when evaluating the student's response.

# What each file contains that created.
**static\lms**
- **course.js** Referenced on the edit_course page. The functionality is implemented in this file.d for delete buttons (topic, label, page and task). Makes api call to delete without reloading the page. Also for update button (topic title). Also buttons to move topics up and down, and within the topic, move the elements inside it up and down (label, page, task). Using javascript, only the affected elements are updated
- **score.js** Referenced in the score_task page. This file implements the functionality to save the teacher's grade and comment on a student's task. Makes api call to update without having to refresh.
- **style.css**

**template\lms**
- **layout.html** Base design of the page. Includes menu.
- **login.html** Template with login form.
- **register.html** Template with registration form.
- **index.html** Shows all active courses in list form. In each row, the title and teacher of the course are shown.
- **my_courses.html** Shows all the user's courses in which the user is a student and shows courses where the user is a teacher. In each row the title and teacher of the course are shown.
- **create_course.html** Page with a form for creating a course.
- **info_course.html** Page that shows information about the course such as title, description, status. In addition, it shows the list of enrolled students and the teacher and statistics of the course, and when the course is inactive, a button to unenroll is shown to the teacher.
- **config_course.html** Page to edit the course, its title, description and status.
- **course.html** Page where the title of the course is shown, with the titles of the topics and within the elements labels, pages and tasks.
- **edit_course.html** Page that is shown only to the teacher. The title of the course is shown, with the titles of the topics and within the elements labels, pages and tasks. He is given the option to order them, edit them, delete them, etc. It is, together with course.html, the most complex pages due to its logic.
- **edit_label.html** Form page for the label resource. This page is used both for creation and for editing.
- **edit_page.html** Form page for the page resource. This page is used for both creation and editing.
- **edit_task.html** Form page for task resource. This page is used for both creation and editing.
- **page.html** Page where the content of the page resource is displayed.
- **task.html** Page where the content of the task is displayed.
- **score_task.html** Page where only the teacher can access and all the answers given by the students to an assignment are displayed. The teacher grades and can leave comments.

**model.py Contains the models**
- **User
- **Course** (title, description, **User** teacher, create_at, state)
- **Enrollment** (**Course** course, **User** user, create_at)
- **Topic** (**Course** course, title, create_at)
- **Label** (**Topic** topic, text_content, create_at)
- **Page** (**Topic** topic, title, text_content, create_at)
- **Task** (**Topic** topic, title, text_content, create_at)
- **Answer** (**Task** task, **User** student, text, create_at)
- **Score** (**Answer** answer, score, explanation, create_at)

**view.py defined functions**

Login, create account, log out
> login_view, logout_view, register

Logic to get all the courses, Logic to obtain all the courses where you are a student or teacher
> index, my_courses

read, create, update and delete course
> course, create_course, edit_course, delete_course

view info of course, edit info of course
> info_course, config_course

create, update and delete topic
> create_topic, update_topic, delete_topic

create, update and delete label
> edit_label, edit_label, delete_label

read, create update and delete page
> page, edit_page, delete_page

read, create update and delete task
> task, edit_task, delete_task

Logic to move topic and Logic to move elements within the topic
> move_topic, move_element

Logic for enrolling a student and Logic for unenrolling students from a course
> enrollment, unrollment

Logic to display assignment grades and Logic to create grade and Logic to update grade
> score_task, create_score, update_score

## How to run your application.
```
pip freeze > requirements.txt
python manage.py makemigrations lms
python manage.py migrate
python manage.py runserver

python manage.py createsuperuser
```
