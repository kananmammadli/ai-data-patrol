from fastapi import APIRouter, HTTPException, Body
from app.core.organization_tree import (
    load_organization_tree, save_organization_tree, add_node, delete_node
)
from app.models.data_quality import OrganizationNode, OrganizationNodeType
from typing import Dict, Any

router = APIRouter(prefix="/organization", tags=["organization"])

@router.get("/tree")
def get_organization_tree():
    return load_organization_tree()

@router.post("/add")
def add_organization_node(
    parent_id: str = Body(None),
    node: Dict[str, Any] = Body(...)
):
    if not node.get("id") or not node.get("name"):
        raise HTTPException(status_code=400, detail="Node must have 'id' and 'name'")
    if not add_node(parent_id, node):
        raise HTTPException(status_code=404, detail="Parent not found")
    return {"success": True}

@router.delete("/delete/{node_id}")
def delete_organization_node(node_id: str):
    if not delete_node(node_id):
        raise HTTPException(status_code=404, detail="Node not found")
    return {"success": True}

@router.post("/export")
def export_organization_tree():
    # Export the org tree as JSON
    from sqlalchemy.orm import joinedload
    from app.core.database import get_db
    import fastapi
    db: fastapi.Depends = next(get_db())
    def build_tree(node):
        return {
            "id": node.id,
            "name": node.name,
            "type": node.type,
            "description": node.description,
            "children": [build_tree(child) for child in node.children]
        }
    roots = db.query(OrganizationNode).filter(OrganizationNode.parent_id == None).all()
    tree = [build_tree(root) for root in roots]
    return tree

@router.post("/import")
def import_organization_tree(tree: list):
    # Import the org tree from JSON
    from app.core.database import get_db
    import fastapi
    db: fastapi.Depends = next(get_db())
    def add_node(node, parent_id=None):
        org_node = OrganizationNode(
            name=node["name"],
            type=node["type"],
            description=node.get("description"),
            parent_id=parent_id
        )
        db.add(org_node)
        db.flush()
        for child in node.get("children", []):
            add_node(child, org_node.id)
    db.query(OrganizationNode).delete()
    for root in tree:
        add_node(root)
    db.commit()
    return {"success": True}
