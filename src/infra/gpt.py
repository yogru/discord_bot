from typing import List

from openai import OpenAI

from src.infra.env import EnvSettings


class GPT:
    """

    """

    def __init__(self, env: EnvSettings):
        # Set up variables
        # OpenAI API model name : gpt-3.5, gpt-3.5-turbo-16k, gpt-4
        # self.version = "gpt-3.5-turbo-16k"  # default gpt-3.5-turbo -> https://platform.openai.com/docs/models/gpt-3-5
        self.version = "gpt-4o"  # default gpt-3.5-turbo -> https://platform.openai.com/docs/models/gpt-3-5
        self.memory = False  # conversation memory 추가 예정 -> langchain 참고
        self.messages = []
        self.env = env

    def clear(self):
        self.messages = []

    def add_messages(self, role, message: str):
        """This function is for adding new messages and returns 'True'"""
        temp = {"role": role, "content": message}
        self.messages.append(temp)
        return temp

    def add_prompt_list(self, prompt_list: List[str]):
        for prompt in prompt_list:
            self.add_messages(
                role='system',
                message=prompt,
            )

    def add_user_message(self, message: str):
        return self.add_messages(
            role='user',
            message=message,
        )

    def compilation(self, temperature=0.0):
        """ returns the answer of the agent"""
        client = OpenAI(api_key=self.env.OPEN_AI_KEY)
        # Set the OpenAI model (OpenAI version is 0.28)
        completion = client.chat.completions.create(model="gpt-4o-2024-11-20",
                                                    messages=self.messages,
                                                    temperature=temperature, max_tokens=1999)
        # completion = openai.ChatCompletion.create(model="gpt-4o", messages=self.message, temperature=temperature, max_tokens = 500)
        # Get the answer as a text
        answer = completion.choices[0].message.content
        return answer
