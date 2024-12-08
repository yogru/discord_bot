import uuid

from src.domain.model import LLMQAEntity, LLMPromptEntity
from src.infra.env import EnvSettings
from src.infra.gpt import GPT
from src.uow import SqlAlchemyUow


class ChatUseCase:
    def __init__(self, uow: SqlAlchemyUow, env: EnvSettings):
        self.uow = uow
        self.gpt_dict = {}
        self.env = env

    def get_gpt(self, user_id: str) -> GPT:
        gpt = self.gpt_dict.get(user_id, None)
        if gpt is None:
            self.gpt_dict[user_id] = GPT(env=self.env)
            return self.gpt_dict[user_id]
        return gpt

    def create_prompt(self, user_id: str, title: str, prompt: str) -> uuid.UUID:
        with self.uow:
            new_prompt = LLMPromptEntity(
                title=title,
                user_id=user_id,
                prompt=prompt,
            )
            self.uow.llm_repo.add(new_prompt)
            self.uow.commit()
            return new_prompt.id

    def create_chat(self, user_id: str, question: str):
        prompt_list = []
        prompt_id_list = []
        with self.uow:
            prompt_entity_list = self.uow.llm_repo.find_prompt_by_user_id(
                user_id=user_id
            )
            prompt_list = [p.prompt for p in prompt_entity_list]
            prompt_id_list = [p.id for p in prompt_entity_list]

        gpt = self.get_gpt(user_id)
        gpt.add_prompt_list(prompt_list)
        gpt.add_user_message(message=question)
        answer = gpt.compilation()
        gpt.clear()
        with self.uow:
            new_id = uuid.uuid4()
            new_llm = LLMQAEntity(
                id=new_id,
                user_id=user_id,
                question=question,
                answer=answer,
            )
            new_llm.add_prompt_list(prompt_id_list)
            self.uow.llm_repo.add(new_llm)
            self.uow.commit()
            return answer
