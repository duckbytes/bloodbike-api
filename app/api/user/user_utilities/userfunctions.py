import functools
import logging
import os
import random
import string
from PIL import Image

from flask_praetorian import utilities
from app import models
from app.api.functions.errors import forbidden_error
from app import cloud_stores
from app.exceptions import ObjectNotFoundError, InvalidFileUploadError
from app import db


def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def user_id_match_or_admin(func):
    @functools.wraps(func)
    def wrapper(self, user_id):
        if 'admin' in utilities.current_rolenames():
            return func(self, user_id)
        user_int_id = models.User.query.filter_by(uuid=user_id).first().id
        if utilities.current_user_id() == user_int_id:
            return func(self, user_id)
        else:
            return forbidden_error("Object not owned by user: user id: {}".format(user_id))

    return wrapper


def get_all_users(filter_deleted=True):
    if filter_deleted:
        return models.User.query.all()
    else:
        return models.User.query.with_deleted().all()


def get_user_object(user_id, with_deleted=False):
    if with_deleted:
        user = models.User.query.with_deleted().filter_by(uuid=user_id).first()
    else:
        user = models.User.query.filter_by(uuid=user_id).first()
    if not user:
        raise ObjectNotFoundError()

    return user


def get_user_object_by_int_id(user_id):
    user = models.User.query.filter_by(id=user_id).first()

    if not user:
        raise ObjectNotFoundError()

    return user

def upload_profile_picture(picture_file_path, user_id, crop_dimensions=None):
    # get the profile pics store ready
    cloud_stores.initialise_profile_pictures_store()
    image = Image.open(picture_file_path)
    if crop_dimensions:
        image = image.crop(crop_dimensions)

    # TODO: make this configurable
    image = image.resize((300, 300))

    # save and convert to jpg here
    cropped_filename = os.path.join(os.path.dirname(picture_file_path), "{}_cropped.jpg".format(picture_file_path))
    thumbnail_filename = os.path.join(os.path.dirname(picture_file_path), "{}_thumbnail.jpg".format(picture_file_path))
    image.save(cropped_filename)
    image = image.resize((128, 128))
    image.save(thumbnail_filename)
    key_name = "{}_{}.jpg".format(os.path.basename(picture_file_path), user_id)
    thumbnail_key_name = "{}_{}_thumbnail.jpg".format(os.path.basename(picture_file_path), user_id)
    profile_picture_store = cloud_stores.get_profile_picture_store()

    profile_picture_store.upload(cropped_filename, key_name, delete_original=True)
    profile_picture_store.upload(thumbnail_filename, thumbnail_key_name, delete_original=True)
    user = get_user_object(user_id)
    user.profile_picture_key = key_name
    user.profile_picture_thumbnail_key = thumbnail_key_name
    db.session.commit()
    try:
        os.remove(picture_file_path)
    except FileNotFoundError:
        logging.warning("File {} does not exist.".format(picture_file_path))
    except Exception as e:
        logging.warning("Could not delete file {}. Reason: {}".format(picture_file_path, e))
    return key_name


def get_presigned_profile_picture_url(user_uuid):
    # get the profile pics store ready
    cloud_stores.initialise_profile_pictures_store()
    user = get_user_object(user_uuid)
    return cloud_stores.get_profile_picture_store.get_presigned_image_url(user.profile_picture_key)
