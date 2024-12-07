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
        self.message = []
        self.env = env

    def add_message(self, role, message: str):
        """This function is for adding new messages and returns 'True'"""
        temp = {"role": role, "content": message}
        self.message.append(temp)
        return True

    def compilation(self, temperature=0.0):
        """ returns the answer of the agent"""
        client = OpenAI(api_key=self.env.OPEN_AI_KEY)
        # Set the OpenAI model (OpenAI version is 0.28)
        completion = client.chat.completions.create(model="gpt-4o",
                                                    messages=self.message,
                                                    temperature=temperature, max_tokens=1500)
        # completion = openai.ChatCompletion.create(model="gpt-4o", messages=self.message, temperature=temperature, max_tokens = 500)
        # Get the answer as a text
        answer = completion.choices[0].message.content
        return answer
