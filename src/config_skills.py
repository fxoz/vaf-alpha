import inspect

from skills._skill_usage import SKILLS

TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _iter_tool_methods(skill):
    skill_class = skill.__class__
    for name, method in inspect.getmembers(skill_class, predicate=inspect.isfunction):
        if name.startswith("_"):
            continue
        if method.__qualname__.split(".")[0] != skill_class.__name__:
            continue
        yield name, getattr(skill, name)


def _get_parameter_info(method: callable) -> dict:
    sig = inspect.signature(method)
    parameters = {}
    required = []

    for param_name, param in sig.parameters.items():
        assert TYPE_MAP.get(param.annotation), (
            f"Unsupported parameter type: {param.annotation}"
        )
        parameters[param_name] = {
            "type": TYPE_MAP[param.annotation],
            "description": ""
            if param.default == inspect.Parameter.empty
            else f"Default: {param.default}",
        }
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return {"type": "object", "properties": parameters, "required": required}


TOOL_REGISTRY = {}
TOOL_DEFINITIONS = []

for skill in SKILLS:
    for name, method in _iter_tool_methods(skill):
        tool_name = f"{skill.__class__.__name__}__{name}"
        TOOL_REGISTRY[tool_name] = method
        TOOL_DEFINITIONS.append(
            {
                "type": "function",
                "name": tool_name,
                "description": method.__doc__ or "",
                "parameters": _get_parameter_info(method),
            }
        )
