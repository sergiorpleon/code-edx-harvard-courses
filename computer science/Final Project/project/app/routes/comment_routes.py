from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import EventForm, EventOccurrenceForm, CommentForm
from app.models import Comment
from flask_login import current_user
from app.helpers import requires_access_level
from app import db
from datetime import datetime
import string

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/event/<int:event_id>/comment', methods=['POST'])
@requires_access_level('viewer')
def create_comment(event_id):
    form = CommentForm()

    # Validate form and create Comment with form data
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,
            date_time=(datetime.now()),
            id_event=event_id,
            id_user=current_user.id
            
        )

        # Add the session new comment and commit the changes to the database
        db.session.add(new_comment)
        db.session.commit()
        
        # Success create message
        flash('Comment created successfully.', 'success')
        #return redirect(url_for('event.view_event', event_id=event_id))
    
    return redirect(url_for('event.view_event', event_id=event_id))

@comment_bp.route('/event/<int:event_id>/delete_comment/<int:comment_id>', methods=['POST'])
@requires_access_level('journalist')
def delete_comment(event_id, comment_id):
    # Get comment by ID
    comment = Comment.query.get_or_404(comment_id)  

    # Delete the session comment and commit the changes to the database
    db.session.delete(comment)  
    db.session.commit()  

    # Success message and Redirect to main page or wherever you want
    flash('Comment successfully deleted.', 'success')  
    return redirect(url_for('event.view_event', event_id=event_id)) 

@comment_bp.route('/more_comments')
def more_commnets():
    # Get page and event request parameter
    page = request.args.get('page', 0, type=int)
    event_id = request.args.get('event', 0, type=int)

    # Get the next 10 comments
    more_comments = Comment.query.filter_by(id_event=event_id).order_by(Comment.date_time.desc()).limit(10).offset(page * 10).all()
    has_more = len(more_comments) == 10
    
    return render_template('partial_comments.html', event_id=event_id, comments=more_comments, has_more=has_more)