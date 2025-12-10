from fastapi.testclient import TestClient
from fastapi_app.main import app
import uuid

client = TestClient(app)

def test_members_register_and_qr():
    payload = {
        "full_name": "Test User",
        "father_name": "Parent",
        "cnic": "CNIC" + uuid.uuid4().hex[:12],
        "phone": "03001234567",
        "city": "City",
        "district": "District",
        "designation": "Member",
        "membership_type": "Standard"
    }
    headers = {"X-API-Key": "dev-key"}
    res = client.post("/members/register", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    mid = data["membership_id"]
    assert isinstance(mid, str)
    q = client.get(f"/qr/{mid}")
    assert q.status_code == 200
    qd = q.json()
    assert qd["membership_id"] == mid
    assert isinstance(qd["qr_base64"], str)

def test_team_crud():
    payload = {
        "full_name": "Team User",
        "father_name": "Parent",
        "cnic": "CNIC" + uuid.uuid4().hex[:12],
        "phone": "03007654321",
        "city": "City",
        "district": "District",
        "designation": "Officer",
        "membership_type": "Standard"
    }
    headers = {"X-API-Key": "dev-key"}
    r = client.post("/members/register", json=payload, headers=headers)
    assert r.status_code == 200
    member_id = r.json()["id"]
    headers = {"X-API-Key": "dev-key"}
    add = client.post("/team/", json={"member_id": member_id, "position_title": "Lead", "order_number": 1, "visible": True}, headers=headers)
    assert add.status_code == 200
    tid = add.json()["id"]
    lst = client.get("/team/")
    assert lst.status_code == 200
    assert isinstance(lst.json(), list)
    upd = client.put(f"/team/{tid}", json={"member_id": member_id, "position_title": "Lead", "order_number": 2, "visible": True}, headers=headers)
    assert upd.status_code == 200
