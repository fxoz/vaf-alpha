from abc import ABC
import os


class Skill(ABC):
    def get_skill_storage_folder(self) -> str:
        """Get the path to the skill's storage folder."""
        skill_name = self.__class__.__name__.lower().replace("skill", "")
        storage_folder = os.path.join("skill-storage", skill_name)
        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)
        return storage_folder
