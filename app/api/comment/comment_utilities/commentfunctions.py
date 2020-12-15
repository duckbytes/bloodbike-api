import functools

from flask_praetorian import utilities
from app import models, schemas
from app.api.functions.errors import forbidden_error
from app.exceptions import ObjectNotFoundError
from flask import json, request
import hashlib
from app.api.comment.comment_utilities.comment_socket_actions import ADD_COMMENT


def comment_author_match_or_admin(func):
    @functools.wraps(func)
    def wrapper(self, _id):
        if 'admin' in utilities.current_rolenames():
            return func(self, _id)
        comment_author = models.Comment.query.filter_by(uuid=_id).first().author_uuid
        if utilities.current_user().uuid == comment_author:
            return func(self, _id)
        else:
            return forbidden_error("Comment {} not owned by user: {}".format(_id, comment_author))

    return wrapper


def get_comment_object(_id, with_deleted=False):
    if with_deleted:
        result = models.Comment.query.with_deleted().filter_by(uuid=_id).first()
    else:
        result = models.Comment.query.filter_by(uuid=_id).first()
    if not result:
        raise ObjectNotFoundError("comment id: {} not found".format(_id))
    return result


def calculate_comments_etag(data):
    comments_schema = schemas.CommentSchema(many=True)
    json_data = json.dumps(comments_schema.dump(data))
    return hashlib.sha1(bytes(json_data, 'utf-8')).hexdigest()


