import json
import os
from typing import Any, Dict

ORG_TREE_PATH = os.path.join(os.path.dirname(__file__), "organization_tree.json")

def load_organization_tree() -> Dict[str, Any]:
    with open(ORG_TREE_PATH, "r") as f:
        return json.load(f)

def save_organization_tree(tree: Dict[str, Any]):
    with open(ORG_TREE_PATH, "w") as f:
        json.dump(tree, f, indent=2)

def find_node_by_id(node, node_id):
    if node.get("id") == node_id:
        return node
    for child in node.get("children", []):
        found = find_node_by_id(child, node_id)
        if found:
            return found
    return None

def add_node(parent_id: str, new_node: Dict[str, Any]) -> bool:
    tree = load_organization_tree()
    if parent_id is None:
        tree["departments"].append(new_node)
        save_organization_tree(tree)
        return True
    for dept in tree["departments"]:
        parent = find_node_by_id(dept, parent_id)
        if parent:
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(new_node)
            save_organization_tree(tree)
            return True
    return False

def delete_node(node_id: str) -> bool:
    tree = load_organization_tree()
    def _delete(nodes):
        for i, node in enumerate(nodes):
            if node["id"] == node_id:
                del nodes[i]
                return True
            if "children" in node and _delete(node["children"]):
                return True
        return False
    if _delete(tree["departments"]):
        save_organization_tree(tree)
        return True
    return False
