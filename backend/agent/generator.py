from system.component_registry import ALLOWED_COMPONENTS

def sanitize_tree(node):
    if not isinstance(node, dict):
        return None

    node.setdefault("props", {})
    node.setdefault("children", [])

    if not isinstance(node["props"], dict):
        node["props"] = {}

    if not isinstance(node["children"], list):
        node["children"] = []

    if node.get("type") not in ALLOWED_COMPONENTS:
        node["type"] = "Card"

    cleaned_children = []
    for child in node["children"]:
        if isinstance(child, dict):
            cleaned_child = sanitize_tree(child)
            if cleaned_child:
                cleaned_children.append(cleaned_child)

    node["children"] = cleaned_children
    return node