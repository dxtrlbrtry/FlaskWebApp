from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify
from flaskwebapp import db
from flaskwebapp.models import Post, Comment, User, Event
from flaskwebapp.events.forms import EventForm
from datetime import datetime, timedelta

events = Blueprint('events', __name__)


# ======================PAGES================
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


@events.route('/events/<int:event_id>/', methods=['GET'])
@events.route('/events/<int:event_id>/<string:view>', methods=['GET'])
@login_required
def event_view(event_id, view='overview'):
    event = Event.query.get_or_404(event_id)
    return render_template('events/'+view+'.html', event=event, view=view)


@events.route('/events/my/', methods=['GET'])
@login_required
def my_events():
    events = Event.query.filter_by(host=current_user)
    return render_template('my_events.html', events=events)


@events.route('/events/invites/', methods=['GET'])
@login_required
def event_invites():
    return render_template('invites.html', invites=current_user.invites)


# ====================REDIRECTS================
@events.route('/events/leave/<int:event_id>', methods=['GET'])
@login_required
def leave_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user not in event.attendants:
        flash('Cannot leave an event you don\'t attend to', 'info')
    else:
        event.attendants.remove(current_user)
        db.session.commit()
        flash(f'You are no longer attending {event.theme}', 'success')
    return redirect(url_for('events.event_view', event_id=event_id))


# ====================CALLS===================
@events.route('/events/join/<int:event_id>', methods=['POST'])
@login_required
def send_event_request(event_id):
    event = Event.query.get_or_404(event_id)
    if len(event.attendants) >= event.maximum_attendants:
        return jsonify({'message': 'Event full', 'category': 'warning'})
    if current_user in event.attendants:
        return jsonify({'message': 'Already attending to this event', 'category': 'info'})
    if current_user in event.join_requests:
        return jsonify({'message': 'Request already sent', 'category': 'warning'})
    event.join_requests.append(current_user)
    db.session.commit()
    return jsonify({'message': 'Request sent', 'category': 'success'})


@events.route('/events/requests/accept/<string:event_id>/<string:attendant_id>/', methods=['POST'])
@login_required
def accept_event_request(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if attendant in event.attendants:
        event.join_requests.remove(attendant)
        return jsonify({'message': 'User already attends to this event', 'category': 'info'})
    event.join_requests.remove(attendant)
    event.attendants.append(attendant)
    db.session.commit()
    return jsonify({'message': 'Request accepted', 'category': 'success'})


@events.route('/events/requests/refuse/<string:event_id>/<string:attendant_id>/', methods=['POST'])
@login_required
def refuse_event_request(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if attendant in event.attendants:
        return jsonify({'message': 'User already attends to this event', 'category': 'warning'})
    event.join_requests.remove(attendant)
    db.session.commit()
    return jsonify({'message': 'Request rejected', 'category': 'success'})


@events.route('/events/remove/<int:event_id>/<int:attendant_id>/', methods=['POST'])
@login_required
def remove_attendant(event_id, attendant_id):
    event = Event.query.get_or_404(event_id)
    attendant = User.query.get_or_404(attendant_id)
    if current_user == attendant:
        return jsonify({'message': 'Cannot remove yourself from the event', 'category': 'warning'})
    event.attendants.remove(attendant)
    db.session.commit()
    return jsonify({'message': 'User removed from event', 'category': 'success'})


@events.route('/events/invite/<int:event_id>/<int:user_id>/', methods=['POST'])
@login_required
def send_invite(event_id, user_id):
    event = Event.query.get_or_404(event_id)
    user = User.query.get_or_404(user_id)
    if user in event.attendants:
        return jsonify({'message': 'User already attends to this event', 'category': 'info'})
    if user in event.join_requests:
        return jsonify({'message': 'User already sent you a request for this event', 'category': 'info'})
    if user in event.invites_sent:
        return jsonify({'message': 'Invite already sent!', 'category': 'info'})
    if user == current_user:
        return jsonify({'message': 'Cannot invite yourself', 'category': 'info'})
    user.invites.append(event)
    db.session.commit()
    return jsonify({'message': 'Invite sent successfully', 'category': 'success'})


@events.route('/events/invite/accept/<int:event_id>/', methods=['POST'])
@login_required
def accept_invite(event_id):
    event = Event.query.get_or_404(event_id)
    if len(event.attendants) >= event.maximum_attendants:
        return jsonify({'message': 'Event is full', 'category': 'danger'})
    if current_user in event.join_requests:
        event.join_requests.remove(current_user)
        return jsonify({'message': 'You already sent a request for this event', 'category': 'success'})
    if current_user in event.attendants:
        current_user.invites.remove(event)
        return jsonify({'message': 'You are already attending to this event', 'category': 'info'})
    current_user.invites.remove(event)
    event.attendants.append(current_user)
    db.session.commit()
    return jsonify({'message': f'You are now attending to {event.theme}.', 'category': 'success'})


@events.route('/events/invite/refuse/<int:event_id>/', methods=['POST'])
@login_required
def refuse_invite(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user in event.attendants:
        current_user.invites.remove(event)
        return jsonify({'message': 'User already attends to this event', 'category': 'info'})
    current_user.invites.remove(event)
    db.session.commit()
    return jsonify({'message': f'Refused invitation for {event.theme}.', 'category': 'success'})
