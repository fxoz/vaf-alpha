# Skills

Skills are the abilities of the AI agent: fetching the current time (`dateandtime`), reading/writing notes (`memory`), etc.

## Developing Skills

- Use the `Skill` base class to create new skills. 
- `Skill.get_skill_storage_folder() -> str` provides a dedicated folder for the skill to store files, if needed. 
- Use `_security.validate_name(name: str)` for folders, files etc. to prevent path traversal and other security issues.

The AI needs to know which skills are available and how to call them. Thus, it is crucial to:

- Heavily utilize type hinting whenever possible.
- Use docstrings to explain how to use a skill.
- Use very descriptive names for methods and parameters.
