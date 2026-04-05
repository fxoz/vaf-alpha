import inspect

from config_skills import SKILLS

TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def get_parameter_info(method: callable) -> dict:
    sig = inspect.signature(method)
    parameters = {}
    required = []

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue

        assert TYPE_MAP.get(param.annotation), (
            f"Unsupported parameter type: {param.annotation}"
        )
        json_type = TYPE_MAP[param.annotation]

        param_info = {
            "type": json_type,
            "description": ""
            if param.default == inspect.Parameter.empty
            else f"Default: {param.default}",
        }
        parameters[param_name] = param_info

        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return {"type": "object", "properties": parameters, "required": required}


def generate() -> list[dict]:
    """Generate a list of tool definitions for all skills."""
    tools = []

    for skill in SKILLS:
        for name, method in inspect.getmembers(
            skill.__class__, predicate=inspect.isfunction
        ):
            if name.startswith("_"):  # ignore private methods
                continue
            if method.__qualname__.split(".")[0] != skill.__class__.__name__:
                continue

            tool = {
                "type": "function",
                "name": f"{skill.__class__.__name__}__{name}",
                "description": method.__doc__ or "",
                "parameters": get_parameter_info(method),
            }
            tools.append(tool)

    return tools
