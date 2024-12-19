from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import EventForm, CommentForm, CategoryForm
from app.models import Event, Category, EventOccurrence, Comment, SurveyResponse
from flask_login import current_user
from app.helpers import requires_access_level
import markdown
from app import db

event_bp = Blueprint('event', __name__)


@event_bp.route('/category/<int:category_id>')
def category_events(category_id):
    category = Category.query.get(category_id)
    # Get all events from the database order by for date
    events = Event.query.filter_by(id_category=category_id).all()
    return render_template('category.html', category=category, events=events)  


@event_bp.route('/create_category', methods=["GET", "POST"])
@requires_access_level('journalist')
def create_category():
    form = CategoryForm()

    # Validate form and create Category with form data
    if form.validate_on_submit():
        new_category = Category(
            name=form.name.data
        )

        # Add the session new category and commit the changes to the database
        db.session.add(new_category)
        db.session.commit()

        # Success create message and redirect home page
        flash('Category created successfully.', 'success')
        
        return redirect(url_for('event.list_events'))
    
    # Render create form
    return render_template('update_category.html', form=form)

@event_bp.route('/delete_category/<int:category_id>', methods=['POST'])
@requires_access_level('journalist')
def delete_category(category_id):
    # Get the category by ID
    category = Category.query.get_or_404(category_id) 

    # Delete the category from the session and Commit the changes to the database
    db.session.delete(category)
    db.session.commit()

    # Success delete message and Redirect list events templates
    flash('Category successfully deleted.', 'success')
    return redirect(url_for('event.list_events'))










@event_bp.route('/')
def index():
    # Get all events from the database order by for date
    events = Event.query.order_by(Event.date.desc()).all()  
    return render_template('index.html', events=events) 

@event_bp.route('/events')
def list_events():
    categories = Category.query.all()
    # Get all events from the database order by for date
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('events.html', categories=categories, events=events)  

@event_bp.route('/create_event', methods=["GET", "POST"])
@requires_access_level('journalist')
def create_event():
    form = EventForm()

    # Validate form and create Event with form data
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            header=form.header.data,
            description=form.description.data,
            date=form.date.data,
            id_user_creator=current_user.id,
            id_category=form.category.data 
        )


        # Add the session new event and commit the changes to the database
        db.session.add(new_event)
        db.session.commit()

        # Success create message and redirect home page
        flash('Event created successfully.', 'success')
        
        # Check press button
        if form.save_and_view.data:
            return redirect(url_for('event.view_event', event_id=new_event.id))  # Redirige a la siguiente etapa
        
        return redirect(url_for('event.list_events'))
    
    # Render create form
    title = "Create Event"
    return render_template('update_event.html', title=title, form=form)

@event_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@requires_access_level('journalist')
def edit_event(event_id):
    # Get the event by ID and Load event data into the form
    event = Event.query.get_or_404(event_id) 
    form = EventForm(obj=event)
    
    # Valid edit form
    if form.validate_on_submit():
        # Update event attributes with form data
        event.name = form.name.data
        event.header = form.header.data
        event.description = form.description.data
        event.date = form.date.data
        event.id_category = form.category.data

        # Save changes to the database
        db.session.commit()  

        # Success updated message and Redirect list events templates
        flash('Event updated successfully.', 'success')

        # Check press button
        if form.save_and_view.data:
            return redirect(url_for('event.view_event', event_id=event.id))  # Redirige a la siguiente etapa
        
        return redirect(url_for('event.list_events'))  
    
    # Update select field of form with event value
    form.category.data = event.id_category
    
    # Render Edit form
    title = "Edit Event"
    return render_template('update_event.html', title=title, form=form)


@event_bp.route('/delete_event/<int:event_id>', methods=['POST'])
@requires_access_level('journalist')
def delete_event(event_id):
    # Get the event by ID
    event = Event.query.get_or_404(event_id) 

    # Delete the event from the session and Commit the changes to the database
    db.session.delete(event)
    db.session.commit()

    # Success delete message and Redirect list events templates
    flash('Event successfully deleted.', 'success')
    return redirect(url_for('event.list_events'))

@event_bp.route('/view_event/<int:event_id>')
def view_event(event_id):
    # Get event by ID
    event = Event.query.get_or_404(event_id)  
    
    # Get all event occurrences from the database
    ocurrences = EventOccurrence.query.filter_by(id_event=event_id).order_by(EventOccurrence.date_time.desc()).all()
    
    # Get first 10 comments from the database
    comments = Comment.query.filter_by(id_event=event_id).order_by(Comment.date_time.desc()).limit(10).offset(0).all()
    has_more = len(comments) == 10

    # Convert header and description event field in html with markdown
    event.mheader = markdown.markdown(event.header)
    event.mdescription = markdown.markdown(event.description)

    cform = CommentForm()
    
    # Run ocurrence to covert text in hmtl wit markdown and count total vote
    for ocurrence in ocurrences:
        ocurrence.mtext = markdown.markdown(ocurrence.text)
        ocurrence.vote = False
        ocurrence.total_vote = sum(len(o.responses) for o in ocurrence.options)

        # Determine if the user has already voted for one of the options in the survey or not.
        if ocurrence.ocurrence_type.value == "survey":
            try:
                exist = SurveyResponse.query.filter_by(id_survey=ocurrence.id, id_user=current_user.id).all()
                if len(exist) > 0:
                    ocurrence.vote = True
            except AttributeError:
                #if not login (current_user.id error) pass
                pass
    
    # Show event view template
    return render_template('view_event.html', event=event, ocurrences=ocurrences, comments=comments, has_more=has_more, page=0, cform=cform)  # Pasa la lista de eventos a la plantilla


