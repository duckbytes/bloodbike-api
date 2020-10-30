from flask import jsonify
from flask_socketio import emit, join_room, leave_room
from app import socketio
from app import app, api_version
import redis
from rq import Queue, Connection
from threading import Lock

thread = None
thread_lock = Lock()

namespace = "/api/{}/subscribe".format(api_version)
namespace_comments = "/api/{}/subscribe_comments".format(api_version)


@socketio.on('subscribe', namespace=namespace)
def subscribe_to_object(obj_uuid):
    join_room(obj_uuid)
    emit('response', {'data': "Subscribed to object with uuid {}.".format(obj_uuid)})


@socketio.on('subscribe_many', namespace=namespace)
def subscribe_to_objects(uuids_list):
    for i in uuids_list:
        join_room(i)
    emit('response', {'data': "Subscribed to {} objects".format(len(uuids_list))})


@socketio.on('unsubscribe_many', namespace=namespace)
def unsubscribe_from_objects(uuids_list):
    for i in uuids_list:
        leave_room(i)
    emit('response', {'data': "Unsubscribed from {} objects".format(len(uuids_list))})


@socketio.on('unsubscribe', namespace=namespace)
def unsubscribe_from_object(obj_uuid):
    leave_room(obj_uuid)
    emit('response', {'data': "Unsubscribed from object with uuid {}.".format(obj_uuid)})


@socketio.on('subscribe', namespace=namespace_comments)
def subscribe_to_comments(obj_uuid):
    join_room(obj_uuid)
    emit('response', {'data': "Subscribed to comments for object with uuid {}.".format(obj_uuid)})


@socketio.on('unsubscribe', namespace=namespace_comments)
def unsubscribe_from_comments(obj_uuid):
    leave_room(obj_uuid)
    emit('response', {'data': "Unsubscribed from comments for object with uuid {}.".format(obj_uuid)})


@socketio.on('connect', namespace=namespace)
def test_connect():
    print("client connected")
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace=namespace)
def test_disconnect():
    print('Client disconnected')


@socketio.on('authenticated', namespace=namespace)
def test_authenticated():
    print('Authed')
