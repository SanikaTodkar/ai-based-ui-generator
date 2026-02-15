from system.component_registry import ALLOWED_COMPONENTS
from system.schema import UINode

def validate_node(node, depth=0):
    if node is None:
        raise ValueError("Node is None")

    if not isinstance(node.type, str):
        raise ValueError("Node type must be a string")

    if node.type not in ALLOWED_COMPONENTS:
        raise ValueError(f"Component '{node.type}' is not allowed.")

    if depth > 5:
        raise ValueError("Max depth exceeded")

    for child in node.children:
        validate_node(child, depth + 1)


def validate_tree(tree_data):
    if not isinstance(tree_data, dict):
        raise ValueError("Tree must be a dict")

    node = UINode(**tree_data)
    validate_node(node)
    return node.dict()
