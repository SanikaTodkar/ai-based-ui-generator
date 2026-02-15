def explainer(plan, new_tree, previous_tree=None):
    intent = plan.get("intent")
    target = plan.get("target_component")

    if intent == "create":
        return (
            "A new dashboard structure was created using a Card component "
            "as the root container."
        )


    if intent == "add" and target:
        return (
            f"The {target} component was added to the existing layout. "
            "No other components were modified."
        )

    if intent == "remove" and target:
        return (
            f"The {target} component was removed from the layout. "
            "All remaining components were preserved."
        )

    if intent == "modify" and target:
        return (
            f"The {target} component properties were updated. "
            "No structural changes were made."
        )

    return "No structural changes were applied."