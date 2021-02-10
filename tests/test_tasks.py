import json

import pytest

from tests.testutils import task_url, is_valid_uuid, print_response, get_object, attr_check, get_test_json
from app import models, schemas

TASK = models.Objects.TASK


@pytest.mark.parametrize("login_role", ["coordinator"])
def test_post_relay(client, login_header, task_obj):
    r = client.post("{}s".format(task_url),
                     data=json.dumps({
                         "relay_previous_uuid": str(task_obj.uuid),
                         "parent_id": task_obj.parent_id
                     }),
                     headers=login_header)
    print_response(r)
    assert r.status_code == 201
    data = json.loads(r.data)
    assert is_valid_uuid(data['uuid'])
    new_task = get_object(TASK, data['uuid'])
    assert new_task.relay_previous_uuid == task_obj.uuid


@pytest.mark.parametrize("login_role", ["coordinator"])
def test_delete_task(client, task_obj, login_header):
    task_uuid = str(task_obj.uuid)
    r = client.delete(
        "{}/{}".format(task_url, task_uuid),
        headers=login_header)
    assert r.status_code == 202
    task_check_obj = get_object(TASK, task_uuid, with_deleted=True)
    assert task_check_obj.deleted


@pytest.mark.parametrize("login_role", ["coordinator"])
def test_restore_task(client, task_obj_soft_deleted, login_header):
    assert task_obj_soft_deleted.deleted
    task_uuid = str(task_obj_soft_deleted.uuid)
    r = client.put(
        "{}/{}/restore".format(task_url, task_uuid),
        headers=login_header
    )
    assert r.status_code == 200
    task_obj_check = get_object(TASK, task_uuid)
    assert not task_obj_check.deleted


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["coordinator"])
@pytest.mark.parametrize("task_status", ["new"])
def test_get_all_tasks(client, login_header, task_objs_assigned):
    r = client.get("{}s".format(task_url, 1),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    r = client.get("{}s".format(task_url),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["rider", "coordinator"])
@pytest.mark.parametrize("task_status", ["new"])
def test_get_assigned_tasks(client, login_header, task_objs_assigned, user_role):
    assigned_user_uuid = str(task_objs_assigned[0].assigned_riders[0].uuid) if user_role == "rider" else str(task_objs_assigned[0].assigned_coordinators[0].uuid)
    r = client.get("{}s/{}?page={}&role={}".format(task_url, assigned_user_uuid, 1, user_role),
                    headers=login_header,)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test with no page given
    r = client.get("{}s/{}?role={}".format(task_url, assigned_user_uuid, user_role),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test page 2
    r = client.get("{}s/{}?page={}&role={}".format(task_url, assigned_user_uuid, 2, user_role),
                   headers=login_header,)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 10


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["coordinator"])
@pytest.mark.parametrize("task_status", ["new"])
def test_get_assigned_tasks_by_new_coordinator(client, login_header, task_objs_assigned, user_role):
    assigned_user_uuid = str(task_objs_assigned[0].assigned_coordinators[0].uuid)
    r = client.get("{}s/{}?page={}&role={}&status={}".format(task_url, assigned_user_uuid, 1, user_role, "new"),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test with no page given
    r = client.get("{}s/{}?role={}&status={}".format(task_url, assigned_user_uuid, user_role, "new"),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test page 2
    r = client.get("{}s/{}?page={}&role={}&status={}".format(task_url, assigned_user_uuid, 2, user_role, "new"),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 10


@pytest.mark.parametrize("login_role", ["coordinator", "rider"])
@pytest.mark.parametrize("user_role", ["coordinator", "rider"])
@pytest.mark.parametrize("task_status", ["new", "active", "picked_up", "delivered", "cancelled", "rejected"])
def test_get_assigned_tasks_by_status(client, login_header, task_objs_assigned, user_role, task_status, login_role):
    if login_role != user_role:
        return
    if user_role == "rider" and task_status == "new":
        return
    assigned_user_uuid = None
    if user_role == "coordinator":
        assigned_user_uuid = str(task_objs_assigned[0].assigned_coordinators[0].uuid)
    if user_role == "rider":
        assigned_user_uuid = str(task_objs_assigned[0].assigned_riders[0].uuid)
    assert assigned_user_uuid

    r = client.get("{}s/{}?page={}&role={}&status={}".format(task_url, assigned_user_uuid, 1, user_role, task_status),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test with no page given
    r = client.get("{}s/{}?role={}".format(task_url, assigned_user_uuid, user_role),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 20
    # test page 2
    r = client.get("{}s/{}?page={}&role={}".format(task_url, assigned_user_uuid, 2, user_role),
                   headers=login_header,)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 10

    # test with page set to 0 (get all)
    r = client.get("{}s/{}?page={}&role={}".format(task_url, assigned_user_uuid, 0, user_role),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 30


@pytest.mark.parametrize("login_role", ["coordinator", "rider"])
@pytest.mark.parametrize("user_role", ["coordinator", "rider"])
@pytest.mark.parametrize("task_status", ["new", "active", "picked_up", "delivered", "cancelled", "rejected"])
def test_get_assigned_tasks_by_status_and_before_parent_id(client, login_header, task_objs_assigned, user_role, task_status, login_role):
    if login_role != user_role:
        return
    if user_role == "rider" and task_status == "new":
        return
    assigned_user_uuid = None
    if user_role == "coordinator":
        assigned_user_uuid = str(task_objs_assigned[0].assigned_coordinators[0].uuid)
    if user_role == "rider":
        assigned_user_uuid = str(task_objs_assigned[0].assigned_riders[0].uuid)
    assert assigned_user_uuid
    parent_id = task_objs_assigned[29].parent_id
    r = client.get(
        "{}s/{}?before_parent={}&role={}&status={}".format(task_url, assigned_user_uuid, parent_id, user_role, task_status),
        headers=login_header
    )
    result = json.loads(r.data)
    assert len(result) == 20
    for i in result:
        assert i['parent_id'] < parent_id

    # test with page set to 2
    r = client.get("{}s/{}?before_parent={}&page={}&role={}".format(task_url, assigned_user_uuid, parent_id, 2, user_role),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 9
    for i in result:
        assert i['parent_id'] < parent_id


    # test with page set to 0 (get all)
    r = client.get("{}s/{}?before_parent={}&page={}&role={}".format(task_url, assigned_user_uuid, parent_id, 0, user_role),
                   headers=login_header)
    assert r.status_code == 200
    result = json.loads(r.data)
    assert len(result) == 29
    for i in result:
        assert i['parent_id'] < parent_id


@pytest.mark.parametrize("login_role", ["coordinator"])
def test_post_task(client, login_header):
    r2 = client.post("{}s".format(task_url),
                     data=json.dumps({}),
                     headers=login_header)
    print_response(r2)
    assert r2.status_code == 201
    assert is_valid_uuid(json.loads(r2.data)['uuid'])


@pytest.mark.parametrize("login_role", ["coordinator"])
def test_update_task(client, login_header, task_data, task_obj, login_role):
    task_uuid = str(task_obj.uuid)
    r3 = client.patch("{}/{}".format(task_url, task_uuid),
                     data=json.dumps(task_data),
                     headers=login_header)
    print_response(r3)
    assert r3.status_code == 200
    obj = get_object(TASK, task_uuid)
    attr_check(task_data, obj, exclude=["timestamp"])


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["rider", "coordinator"])
def test_task_assignment_get(client, login_header, task_obj_assigned, user_role):
    assignee_uuid = str(task_obj_assigned.assigned_riders[0].uuid) if user_role == "rider" else str(task_obj_assigned.assigned_coordinators[0].uuid)
    r = client.get("{}/{}/assigned_users?role={}".format(task_url, task_obj_assigned.uuid, user_role),
                   headers=login_header)
    assert r.status_code == 200
    user_uuid = json.loads(r.data)[0]['uuid']
    assert user_uuid == assignee_uuid


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["rider", "coordinator"])
def test_task_assignment_put(client, login_header, task_obj, user_obj, user_role):
    assignee_uuid = str(user_obj.uuid)
    task_uuid = str(task_obj.uuid)
    data = {"user_uuid": assignee_uuid}
    r = client.put("{}/{}/assigned_users?role={}".format(task_url, task_uuid, user_role),
                   data=json.dumps(data),
                   headers=login_header)
    assert r.status_code == 200
    r = client.get("{}/{}/assigned_users?role={}".format(task_url, task_uuid, user_role),
                   headers=login_header)
    assert r.status_code == 200
    user_uuid = json.loads(r.data)[0]['uuid']
    assert user_uuid == assignee_uuid


@pytest.mark.parametrize("login_role", ["coordinator"])
@pytest.mark.parametrize("user_role", ["rider", "coordinator"])
def test_task_assignment_delete(client, login_header, task_obj_assigned, user_role):
    task_uuid = str(task_obj_assigned.uuid)
    assignee_uuid = None
    if user_role == "rider":
        assignee_uuid = str(task_obj_assigned.assigned_riders[0].uuid)
    elif user_role == "coordinator":
        assignee_uuid = str(task_obj_assigned.assigned_coordinators[0].uuid)

    assert assignee_uuid

    r = client.delete(
        "{}/{}/assigned_users?role={}".format(task_url, task_uuid, user_role),
        headers=login_header,
        data=json.dumps({"user_uuid": assignee_uuid})
    )
    assert r.status_code == 200
    new_task = get_object(TASK, task_uuid)
    if user_role == "rider":
        assert assignee_uuid not in [str(u.uuid) for u in new_task.assigned_riders]
    elif user_role == "coordinator":
        assert assignee_uuid not in [str(u.uuid) for u in new_task.assigned_coordinators]


@pytest.mark.parametrize("destination_location", ["pickup", "delivery"])
@pytest.mark.parametrize("login_role", ["coordinator", "rider"])
def test_get_task(client, login_header, task_obj_address_preset):
    task_uuid = str(task_obj_address_preset.uuid)
    r = client.get(
        "{}/{}".format(task_url, task_uuid),
        headers=login_header
    )
    assert r.status_code == 200


@pytest.mark.parametrize("destination_location", ["pickup", "delivery"])
@pytest.mark.parametrize("login_role", ["coordinator"])
def test_task_assign_saved_location(client, login_header, destination_location, location_obj, task_obj):
    task_uuid = str(task_obj.uuid)
    address_schema = schemas.AddressSchema()
    r = client.put(
        "{}/{}/destinations?destination={}".format(task_url, task_uuid, destination_location),
        headers=login_header,
        data=json.dumps({"location_uuid": str(location_obj.uuid)}))
    assert r.status_code == 200
    obj = get_object(TASK, task_uuid)
    if destination_location == "pickup":
        assert obj.pickup_location_uuid == location_obj.uuid
        attr_check(address_schema.dump(location_obj.address), obj.pickup_address)
    else:
        assert obj.dropoff_location_uuid == location_obj.uuid
        attr_check(address_schema.dump(location_obj.address), obj.dropoff_address)


@pytest.mark.parametrize("destination_location", ["pickup", "delivery"])
@pytest.mark.parametrize("login_role", ["coordinator"])
def test_task_unassign_saved_location(client, login_header, destination_location, task_obj_address_preset):
    task_uuid = str(task_obj_address_preset.uuid)
    if destination_location == "pickup":
        assert task_obj_address_preset.pickup_location_uuid
    else:
        assert task_obj_address_preset.dropoff_location_uuid
    r = client.delete(
        "{}/{}/destinations?destination={}".format(task_url, task_uuid, destination_location),
        headers=login_header)
    assert r.status_code == 200
    obj = get_object(TASK, task_uuid)
    if destination_location == "pickup":
        assert not obj.pickup_location_uuid
    else:
        assert not obj.dropoff_location_uuid


@pytest.mark.parametrize("destination_location", ["pickup"])
@pytest.mark.parametrize("login_role", ["coordinator"])
def test_task_restrict_changing_address_on_preset_location(client, login_header, task_obj_address_preset, destination_location):
    task_uuid = str(task_obj_address_preset.uuid)
    if destination_location == "pickup":
        r = client.patch(
            "{}/{}".format(task_url, task_uuid),
            headers=login_header,
            data=json.dumps({"pickup_address": get_test_json()['savedlocations'][0]['address']}))
        task_test = get_object(TASK, task_uuid)
        assert task_test.pickup_location.address_id == task_obj_address_preset.pickup_location.address_id
        assert r.status_code == 403
    elif destination_location == "delivery":
        r = client.patch(
            "{}/{}".format(task_url, task_uuid),
            headers=login_header,
            data=json.dumps({"dropoff_address": get_test_json()['savedlocations'][0]['address']}))
        assert r.status_code == 403


@pytest.mark.parametrize("destination_location", ["pickup", "delivery", "both"])
@pytest.mark.parametrize("login_role", ["coordinator"])
def test_get_task_destinations(client, login_header, task_obj_addressed, destination_location):
    task_uuid = str(task_obj_addressed.uuid)
    r = client.get(
        "{}/{}/destinations?destination={}".format(task_url, task_uuid, destination_location),
        headers=login_header
    )
    assert r.status_code == 200
    result = json.loads(r.data)
    print(result)
    if destination_location == "pickup":
        attr_check(result, task_obj_addressed.pickup_address)
    elif destination_location == "delivery":
        attr_check(result, task_obj_addressed.dropoff_address)
    else:
        attr_check(result["pickup"], task_obj_addressed.pickup_address)
        attr_check(result["dropoff"], task_obj_addressed.dropoff_address)

