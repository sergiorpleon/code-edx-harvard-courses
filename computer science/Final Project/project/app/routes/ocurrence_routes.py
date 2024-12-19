from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import EventForm, EventOccurrenceForm
from app.models import Event, EventOccurrence, OcurrenceTypeEnum, SurveyOption, SurveyResponse
from flask_login import current_user
from app.helpers import requires_access_level
from app import db, socketio
from datetime import datetime
import string

ocurrence_bp = Blueprint('ocurrence', __name__)


@ocurrence_bp.route('/event/<int:event_id>/create_ocurrence', methods=['GET', 'POST'])
@requires_access_level('journalist')
def create_ocurrence(event_id):
    form = EventOccurrenceForm()
    event = Event.query.get(event_id)
    
    # Validate form and create Event Ocurrence with form data
    if form.validate_on_submit():
        new_occurrence = EventOccurrence(
            text=form.text.data,
            ocurrence_type=OcurrenceTypeEnum[form.ocurrence_type.data],
            date_time=(datetime.now()),
            id_event=event_id,
            id_user=current_user.id
            
        )

        # Add the session new event ocurrence and commit the changes to the database
        db.session.add(new_occurrence)
        db.session.commit()

        # Add survey options to session if have
        if new_occurrence.ocurrence_type.value == "survey":
            for option in form.options:
                if option.option.data:
                    new_option = SurveyOption(option=option.option.data, id_survey=new_occurrence.id)
                    db.session.add(new_option)
        
            db.session.commit()  

        # Broadcast event to all connected users
        socketio.emit('new_ocurrence', {'new_ocurrence': True})

        # Successful creation message and Redirect to a page that shows the occurrences
        flash('Event ocurrence created successfully.', 'success')
        return redirect(url_for('event.view_event', event_id=event_id)) 
    else:
        # Print errors for debugging
        print(form.errors)
    
    title="Create Event Ocurrence (Narration/Survey)"
    return render_template('update_ocurrence.html', event_id=event_id, title=title, form=form)

@ocurrence_bp.route('/event/<int:event_id>/edit_event/<int:ocurrence_id>', methods=['GET', 'POST'])
@requires_access_level('journalist')
def edit_ocurrence(event_id, ocurrence_id):
    # Get the event ocurrence by ID and Load event ocurrence data into the form
    ocurrence = EventOccurrence.query.get_or_404(ocurrence_id)
    form = EventOccurrenceForm(obj=ocurrence)
    
    if form.validate_on_submit():
        # Update event ocurrence attributes in form data
        ocurrence.text = form.text.data
        ocurrence.ocurrence_type = OcurrenceTypeEnum[form.ocurrence_type.data]
        
        # Save changes to the database
        db.session.commit() 
        
        # Broadcast event to all connected users
        socketio.emit('edit_ocurrence', {'edit_ocurrence': True})
        
        flash('Event Ocurrence updated successfully.', 'success')
        return redirect(url_for('event.view_event', event_id=event_id))

    # Update form select with ocurrence type data
    form.ocurrence_type.data = ocurrence.ocurrence_type.name

    title = "Edit Event Ocurrence"+ocurrence.ocurrence_type.value    
    return render_template('update_ocurrence.html', event_id=event_id, title=title, form=form)

@ocurrence_bp.route('/event/<int:event_id>/delete_ocurrence/<int:ocurrence_id>', methods=['POST'])
@requires_access_level('journalist')
def delete_ocurrence(event_id, ocurrence_id):
    # Get the event ocurrence by ID and Delete the event ocurrence from the session
    ocurrence = EventOccurrence.query.get_or_404(ocurrence_id)  
    
    # Delete ofsession and Commit changes to the database
    db.session.delete(ocurrence)  
    db.session.commit()  


    flash('Event Ocurrence successfully deleted.', 'success')
    return redirect(url_for('event.view_event', event_id=event_id)) 


@ocurrence_bp.route('/event/<int:event_id>/vote_ocurrence/<int:ocurrence_id>/', methods=['GET'])
def vote_ocurrence(event_id, ocurrence_id):
    # Get event ocurrence by ID
    ocurrence = EventOccurrence.query.get(ocurrence_id)

    if ocurrence.ocurrence_type.value == "survey":
        return render_template('survey.html', event_id=event_id, ocurrence=ocurrence)
    
    return redirect(url_for('event.view_event', event_id=event_id))


@ocurrence_bp.route('/event/<int:event_id>/ocurrence/<int:ocurrence_id>/option/<int:option_id>', methods=['POST'])
@requires_access_level('viewer')
def vote(event_id, ocurrence_id, option_id):
    # Get event ocurrence by ID and get vote if exist
    ocurrece = EventOccurrence.query.get(ocurrence_id)
    exist = SurveyResponse.query.filter_by(id_survey=ocurrence_id, id_user=current_user.id).all()
    
    # If not exist vote and event ocurrence is type survey, create te vote
    if not exist and ocurrece.ocurrence_type.value=="survey":
        new_vote = SurveyResponse(
            date_time=(datetime.now()),
            id_survey=ocurrence_id,
            id_option=option_id,
            id_user=current_user.id  
        )

        # Add vote session and Commit changes to the database
        db.session.add(new_vote)
        db.session.commit()
        
        flash("Voted survey.")
    
    return redirect(url_for('event.view_event', event_id=event_id))

# Crud type
# +Filer pagina de inicio por type
# Event preview, etc

# Commnet template and build style css
# Valid
# Añadir test


