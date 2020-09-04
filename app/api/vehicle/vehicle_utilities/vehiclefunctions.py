from app import models
from app.exceptions import ObjectNotFoundError


def get_vehicle_object(_id):
    vehicle = models.Vehicle.query.filter_by(uuid=_id).first()
    if not vehicle:
        raise ObjectNotFoundError()
    return vehicle


def get_all_vehicles(filter_deleted=False):
    if filter_deleted:
        return models.Vehicle.query.filter_by(flagged_for_deletion=False)
    else:
        return models.Vehicle.query.all()
