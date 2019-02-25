from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flaskwebapp import db
from flaskwebapp.models import Post, Comment, User, Event
from flaskwebapp.events.forms import EventForm
from flaskwebapp.posts.utils import post_photo
import json

events = Blueprint('events', __name__)


@events.route('/events/new/', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(theme=form.theme.data, start_time=form.start_time.data, end_time=form.end_time.data, hosted_by=current_user)
        if form.description.data:
            event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_event.html', title='New Event', form=form)


@events.route('/events/get/', methods=['GET'])
@login_required
def get_events():
    events = Event.query.all()
    json_events = {}
    for event in events:
        json_events.append()
    altceva = json.dumps({'events': events})
    return ceva
