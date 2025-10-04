from env import ENV
from chatbot import ChatBot

environment = ENV.getInstance()
bot = ChatBot.getInstance()

print(environment.GEMINI_API_KEY)
print(bot.testPrompt())
