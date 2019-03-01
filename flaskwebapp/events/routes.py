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
            host=current_user,
            attendants=[current_user],
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
    events = Event.query.all()
    return render_template('events_list.html', events=events)


@events.route('/events/join/<int:event_id>', methods=['GET'])
@login_required
def send_event_request(event_id):
    event = Event.query.get_or_404(event_id)
    if len(event.attendants) >= event.maximum_attendants:
        flash('Event full', 'danger')
    elif current_user in event.attendants:
        flash('Already attending to this event', 'info')
    elif current_user in event.join_requests:
        flash('Request already sent', 'warning')
    else:
        event.join_requests.append(current_user)
        db.session.commit()
    return redirect(url_for('events.events_list'))


@events.route('/events/leave/<int:event_id>', methods=['GET'])
@login_required
def leave_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user not in event.attendants:
        flash('Cannot leave an event you don\'t attend to', 'info')
    else:
        event.attendants.remove(current_user)
        db.session.commit()
    return redirect(url_for('events.events_list'))


@events.route('/events/requests/', methods=['GET'])
@login_required
def event_requests():
    return render_template('event_requests.html', events=current_user.hosted_events)


@events.route('/events/requests/accept/<string:event_id>/<string:attendant_id>/', methods=['POST'])
@login_required
def accept_event_request(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if attendant in event.attendants:
        flash('User already attends to this event')
        event.join_requests.remove(attendant)
    else:
        event.join_requests.remove(attendant)
        event.attendants.append(attendant)
    db.session.commit()
    return redirect(url_for('events.event_requests'))


@events.route('/events/requests/refuse/<string:event_id>/<string:attendant_id>/', methods=['POST'])
@login_required
def refuse_event_request(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if attendant in event.attendants:
        flash('User already attends to this event', 'danger')
    else:
        event.join_requests.remove(attendant)
    db.session.commit()
    return redirect(url_for('events.event_requests'))


@events.route('/events/<int:event_id>', methods=['GET'])
@login_required
def event_view(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_view.html', event=event)


@events.route('/events/remove/<int:event_id>/<int:attendant_id>/', methods=['GET'])
@login_required
def remove_attendant(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if current_user == attendant:
        flash('Cannot remove yourself from the event', 'info')
    else:
        event.attendants.remove(attendant)
        db.session.commit()
    return redirect(url_for('events.event_view', event_id=event_id))


@events.route('/events/my/', methods=['GET'])
@login_required
def my_events():
    events = Event.query.filter_by(host=current_user)
    return render_template('my_events.html', events=events)
