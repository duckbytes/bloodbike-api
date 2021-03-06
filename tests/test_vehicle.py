import json

import pytest

from tests.testutils import dict_check, vehicle_url, \
    is_valid_uuid, get_object, attr_check
from app import db, schemas
from app import models
from datetime import datetime

VEHICLE = models.Objects.VEHICLE


def convert_dates(data):
    data['date_of_manufacture'] = datetime.strptime(data['date_of_manufacture'], '%d/%m/%Y').date()
    data['date_of_registration'] = datetime.strptime(data['date_of_registration'], '%d/%m/%Y').date()
    return data


@pytest.mark.parametrize("login_role", ["admin"])
def test_add_new_vehicle(client, login_header, vehicle_data):
    r = client.post("{}s".format(vehicle_url),
                    data=json.dumps(vehicle_data),
                    headers=login_header)
    new_uuid = r.json['uuid']
    obj = get_object(VEHICLE, new_uuid)
    assert r.status_code == 201
    assert is_valid_uuid(new_uuid)
    check_data = vehicle_data.copy()
    check_data = convert_dates(check_data)
    attr_check(check_data, obj, exclude=["time_created", "time_modified", "links", "comments"])
    db.session.delete(obj)
    db.session.commit()


@pytest.mark.parametrize("login_role", ["admin"])
def test_update_new_vehicle(client, login_header, vehicle_data, vehicle_data_alternative, vehicle_obj):
    vehicle_schema = schemas.VehicleSchema(exclude=("links",))
    vehicle_uuid = str(vehicle_obj.uuid)
    vehicle_dict = vehicle_schema.dump(vehicle_obj)
    vehicle_dict['uuid'] = vehicle_dict['uuid']
    check_data = convert_dates(vehicle_dict)
    attr_check(check_data, vehicle_obj, exclude=["time_created", "time_modified", "links", "comments"])
    r = client.patch("{}/{}".format(vehicle_url, vehicle_uuid),
                   data=json.dumps(vehicle_data_alternative),
                   headers=login_header)
    assert r.status_code == 200
    obj_updated = get_object(VEHICLE, vehicle_uuid)
    check_new_data = vehicle_data_alternative.copy()
    check_new_data['name'] = obj_updated.name
    check_new_data = convert_dates(check_new_data)
    attr_check(check_new_data, obj_updated, exclude=["time_created", "time_modified", "timestamp", "links", "comments"])


@pytest.mark.parametrize("login_role", ["rider", "coordinator", "admin"])
def test_get_vehicle(client, login_header, vehicle_data, vehicle_obj):
    r = client.get("{}/{}".format(vehicle_url, str(vehicle_obj.uuid)),
                   headers=login_header)
    assert r.status_code == 200
    check_data = vehicle_data.copy()
    check_data['name'] = vehicle_obj.name
    dict_check(r.json, check_data, exclude=["time_created", "time_modified", "links", "comments"])


@pytest.mark.parametrize("login_role", ["admin"])
def test_delete_vehicle_admin(client, login_header, vehicle_obj):
    vehicle_uuid = str(vehicle_obj.uuid)
    r = client.delete("{}/{}".format(vehicle_url, vehicle_uuid),
                      headers=login_header)
    assert r.status_code == 202
    vehicle_deleted = get_object(VEHICLE, vehicle_uuid, with_deleted=True)
    assert vehicle_deleted.deleted
    r2 = client.get("{}/{}".format(vehicle_url, vehicle_uuid),
                    headers=login_header)
    assert r2.status_code == 404


@pytest.mark.parametrize("login_role", ["rider", "coordinator"])
def test_delete_vehicle_others(client, login_header, vehicle_obj):
    vehicle_uuid = str(vehicle_obj.uuid)
    r = client.delete("{}/{}".format(vehicle_url, str(vehicle_uuid)),
                      headers=login_header)
    assert r.status_code == 403
    vehicle_new = get_object(VEHICLE, vehicle_uuid, with_deleted=True)
    assert not vehicle_new.deleted
