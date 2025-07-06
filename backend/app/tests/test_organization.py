import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_organization_tree_crud():
    # Initially empty
    resp = client.get("/organization/tree")
    assert resp.status_code == 200
    assert resp.json() == {"departments": []}

    # Add root department
    dept = {"id": "dept1", "name": "Engineering", "type": "department"}
    resp = client.post("/organization/add", json={"parent_id": None, "node": dept})
    assert resp.status_code == 200
    
    # Add sub-department
    sub_dept = {"id": "dept2", "name": "Data", "type": "department"}
    resp = client.post("/organization/add", json={"parent_id": "dept1", "node": sub_dept})
    assert resp.status_code == 200

    # Add project (leaf)
    project = {"id": "proj1", "name": "Data Quality", "type": "project"}
    resp = client.post("/organization/add", json={"parent_id": "dept2", "node": project})
    assert resp.status_code == 200

    # Get tree and check structure
    tree = client.get("/organization/tree").json()
    assert any(d["id"] == "dept1" for d in tree["departments"])

    # Delete project
    resp = client.delete("/organization/delete/proj1")
    assert resp.status_code == 200

    # Delete sub-department
    resp = client.delete("/organization/delete/dept2")
    assert resp.status_code == 200

    # Delete root department
    resp = client.delete("/organization/delete/dept1")
    assert resp.status_code == 200
