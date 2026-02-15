import json
import re
from system.component_registry import ALLOWED_COMPONENTS


def extract_numbers(text):
    rows = None
    columns = None

    row_match = re.search(r'(\d+)\s*rows?', text, re.IGNORECASE)
    col_match = re.search(r'(\d+)\s*columns?', text, re.IGNORECASE)

    if row_match:
        rows = int(row_match.group(1))

    if col_match:
        columns = int(col_match.group(1))

    return rows, columns


def extract_button_label(text):
    words = text.lower().split()
    if "button" in words:
        idx = words.index("button")
        if idx > 0:
            return words[idx - 1].capitalize()
    return None


def clean_node(node):
    if not isinstance(node, dict):
        return None

    node_type = node.get("type")
    if not isinstance(node_type, str):
        return None

    if node_type not in ALLOWED_COMPONENTS:
        return None

    props = node.get("props")
    if not isinstance(props, dict):
        props = {}

    children = node.get("children")
    if not isinstance(children, list):
        children = []

    cleaned_children = []
    for child in children:
        cleaned_child = clean_node(child)
        if cleaned_child:
            cleaned_children.append(cleaned_child)

    return {
        "type": node_type,
        "props": props,
        "children": cleaned_children
    }


def planner(client, user_input):
    with open("prompts/planner_prompt.txt", "r") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    try:
        content = response.choices[0].message.content
        plan = json.loads(content)

        cleaned = []
        for node in plan.get("nodes", []):
            cleaned_node = clean_node(node)
            if cleaned_node:
                cleaned.append(cleaned_node)

        plan["nodes"] = cleaned

        rows, columns = extract_numbers(user_input)
        button_label = extract_button_label(user_input)

        for node in plan.get("nodes", []):
            if node.get("type") == "Table":
                node.setdefault("props", {})
                if rows:
                    node["props"]["rows"] = rows
                if columns:
                    node["props"]["columns"] = columns

            if node.get("type") == "Button":
                node.setdefault("props", {})
                if "label" not in node["props"] and button_label:
                    node["props"]["label"] = button_label

        return plan

    except Exception:
        print("Planner raw output:", response)
        raise Exception("Invalid JSON returned from planner")
