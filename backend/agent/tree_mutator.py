import copy
from system.component_registry import ALLOWED_COMPONENTS

def create_default_tree():
    return {
        "type": "Card",
        "props": {"title": "Dashboard"},
        "children": [
            {
                "type": "Navbar",
                "props": {},
                "children": []
            },
            {
                "type": "Sidebar",
                "props": {},
                "children": []
            }
        ]
    }

# --- Core Mutation Functions --- #

def find_component(node, component_type):
    if node["type"] == component_type:
        return node

    for child in node.get("children", []):
        found = find_component(child, component_type)
        if found:
            return found

    return None

def add_component(tree, component_type, parent_component=None):

    if component_type not in ALLOWED_COMPONENTS:
        return tree

    new_node = {
        "type": component_type,
        "props": get_default_props(component_type),
        "children": []
    }

    if parent_component:
        parent_node = find_component(tree, parent_component)
        if parent_node:

            for child in parent_node["children"]:
                if child["type"] == component_type:
                    return tree

            parent_node["children"].append(new_node)
            return tree

    for child in tree["children"]:
        if child["type"] == component_type:
            return tree

    tree["children"].append(new_node)
    return tree


def remove_component(node, component_type):

    node["children"] = [
        child for child in node.get("children", [])
        if child["type"] != component_type
    ]

    for child in node.get("children", []):
        remove_component(child, component_type)

    return node



def modify_component(node, component_type, details=""):

    if node["type"] == component_type:

        # Modal visibility
        if component_type == "Modal":
            if "open" in details.lower() or "visible" in details.lower():
                node["props"]["visible"] = True
            elif "close" in details.lower() or "hide" in details.lower():
                node["props"]["visible"] = False

        # Chart type
        if component_type == "Chart":
            if "bar" in details.lower():
                node["props"]["type"] = "bar"
            elif "line" in details.lower():
                node["props"]["type"] = "line"
            elif "pie" in details.lower():
                node["props"]["type"] = "pie"

        # Button
        if component_type == "Button":
            if "primary" in details.lower():
                node["props"]["variant"] = "primary"
            elif "secondary" in details.lower():
                node["props"]["variant"] = "secondary"

            if "label:" in details.lower():
                parts = details.split("label:")
                if len(parts) > 1:
                    node["props"]["label"] = parts[1].strip()

        # Card title
        if component_type == "Card":
            if "title:" in details.lower():
                parts = details.split("title:")
                if len(parts) > 1:
                    node["props"]["title"] = parts[1].strip()

        node["props"]["modified"] = True

    # Recurse into children
    for child in node.get("children", []):
        modify_component(child, component_type, details)

    return node


def get_default_props(component_type):

    defaults = {
        "Button": {"label": "Click", "variant": "default"},
        "Card": {"title": "Section"},
        "Input": {"placeholder": "Enter text"},
        "Table": {"headers": [], "rows": []},
        "Modal": {"visible": False},
        "Sidebar": {},
        "Navbar": {},
        "Chart": {"type": "line"}

    }

    return defaults.get(component_type, {})


def mutate_tree(previous_tree, plan):

    tree = copy.deepcopy(previous_tree)

    intent = plan.get("intent")
    target = plan.get("target_component")
    multiple = plan.get("multiple_components", [])
    details = plan.get("details", "")

    if intent in ["add", "create"]:

        if multiple:
            for comp in multiple:
                tree = add_component(tree, comp)
            return tree

        if target:
            return add_component(tree, target)

    if intent == "remove" and target:
        return remove_component(tree, target)

    if intent == "modify" and target:
        return modify_component(tree, target, details)

    return tree
