from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot("Terminal",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapter=[
        'chatterbot.logic.SpecificResponseAdapter',
        'chatterbot.logic.LowConfidenceAdapter',
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="../database.db"
)

bot.storage.drop()
bot.set_trainer(ListTrainer)

bot.train([
    "Ansr",
    "That's what they call me. Automatic Neural System Reponse. Anything I could help you with?",
])

bot.train([
    "Hi",
    "Hello there. What can I help you with today?",
])

bot.train([
    "Help me with",
    "Sure, what do you need?",
])

bot.train([
    "Help",
    "Sure, what do you need?",
])

bot.train([
    "I need help with",
    "Sure, what do you need?",
])

bot.train([
    "Yo",
    "Hello there. What can I help you with today?",
])

bot.train([
    "What is",
    "Let me look into that.. Could you be more specific?",
])

bot.train([
    "What is",
    "What do you mean exactly?",
])

bot.train([
    "What is",
    "Can you elaborate?",
])

bot.train([
    "Who are you?",
    "I'm Ansr, the Automatic Neural System Reponse. What can I help you with?",
])

print("Hi I'm Ansr. I'm the ultimate resource for ulti handbook questions. What can I help you with today?")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Till next time! Goodbye.")
        break
