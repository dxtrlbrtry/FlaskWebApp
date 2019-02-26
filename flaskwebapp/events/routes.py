from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flaskwebapp import db
from flaskwebapp.models import Post, Comment, User, Event
from flaskwebapp.events.forms import EventForm

events = Blueprint('events', __name__)


@events.route('/events/new/', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        start_time = form.event_date.data + ' ' + form.start_time.data
        event = Event(theme=form.theme.data, start_time=start_time, duration=form.duration.data, hosted_by=current_user)
        if form.description.data:
            event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('events_list.home'))
    return render_template('create_event.html', title='New Event', form=form)


@events.route('/events/get/', methods=['GET'])
@login_required
def events_list():
    events = Event.query.order_by(Event.start_time.desc())
    return render_template('events_list.html', events=events)

