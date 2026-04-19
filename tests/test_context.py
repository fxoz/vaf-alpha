from .. import src

from rich import print

chat = src.context.Chat()
chat.add_user_message("2+2")
chat.add_ai_message("2+2 is 4.")

print(chat.get_context())
