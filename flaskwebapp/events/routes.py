from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flaskwebapp import db
from flaskwebapp.models import Post, Comment, User, Event
from flaskwebapp.events.forms import EventForm
from datetime import datetime, timedelta

events = Blueprint('events', __name__)


@events.route('/events/new/', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        end_time = form.start_date.data + timedelta(hours=form.duration_hours.data, minutes=form.duration_minutes.data)
        event = Event(
            theme=form.theme.data,
            start_time=form.start_date.data,
            end_time=end_time,
            hosted_by=current_user,
            location_name=form.location_name.data,
            maximum_attendants=form.maximum_attendants.data)
        if form.description.data:
            event.description = form.description.data
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('events.events_list'))
    return render_template('create_event.html', title='New Event', form=form)


@events.route('/events/', methods=['GET'])
@login_required
def events_list():
    events = Event.query.order_by(Event.start_time.asc())
    return render_template('events_list.html', events=events)


@events.route('/events/join/<int:event_id>', methods=['GET'])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user in event.host.event_requests:
        flash(f'Request already sent', 'warning')
    elif current_user in event.attendants:
        event.event_request_of.remove(current_user)
        flash(f'Successfully left event', 'warning')
    else:
        event.event_request_of.append(current_user)
    db.session.commit()
    return redirect(url_for('events.events_list'))


@events.route('/events/join_request/<int:event_id>', methods=['POST'])
@login_required
def join_request(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user in event.host.event_requests:
        flash(f'Request already sent', 'warning')
    elif current_user in event.attendants:
        flash(f'Your request was already accepted', 'warning')
    else:
        event.host.event_requests.append(current_user)
        db.session.commit()
    return redirect(url_for('events.events_list'))
