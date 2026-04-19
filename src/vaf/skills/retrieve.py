from ._base import Skill


class RetrieveSkill(Skill):
    def retrieve_context(self, id: str) -> str:
        raise NotImplementedError()
