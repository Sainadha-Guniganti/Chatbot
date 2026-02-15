from langchain_core.prompts import ChatPromptTemplate
import pkgutil

from chatbot import prompts


def load_prompt(reference_path:str = "chatbot.prompts", file_name:str = None) ->str | None:
    data = pkgutil.get_data(reference_path, file_name).decode("utf-8")
    return data if data else ""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", load_prompt(file_name = "chatbot_system_prompt.txt")),
    ("user", load_prompt(file_name = "chatbot_user_prompt.txt"))
])

