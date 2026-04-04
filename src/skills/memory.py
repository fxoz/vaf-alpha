from ._base import Skill
from ._safety import validate_name

import os
import pathlib


class MemorySkill(Skill):
    def list_all(self) -> list[str]:
        """List all memories."""
        return [
            f.stem.split(".")[0]
            for f in pathlib.Path(self.get_skill_storage_folder()).glob("*.txt")
        ]

    def write(self, name: str, content: str) -> None:
        """Write (or overwrite) a memory."""
        name = validate_name(name)
        with open(
            os.path.join(self.get_skill_storage_folder(), f"{name}.txt"), "w"
        ) as f:
            f.write(content)

    def read(self, name: str) -> str:
        """Read a memory's contents."""
        name = validate_name(name)
        with open(
            os.path.join(self.get_skill_storage_folder(), f"{name}.txt"), "r"
        ) as f:
            return f.read()
