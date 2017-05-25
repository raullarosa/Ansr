from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

context = [] # passed to ML Engine
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapter=[
        'chatterbot.logic.SpecificResponseAdapter',
        'chatterbot.logic.LowConfidenceAdapter',
        #ML Adapter
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter", #
    database="../database.db",
    read_only=True
)

# bot.storage.drop()
bot.set_trainer(ListTrainer)

bot.train([
    "Hi",
    "Hello there. What can I help you with today?",
])

bot.train([
    "Ansr",
    "That's what they call me. Automatic Neural System Reponse. Anything I could help you with?",
])

bot.train([
    "Who are you?",
    "I'm Ansr, the Automatic Neural System Reponse. What can I help you with?",
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
    "I have a question about",
    "Hit me",
])

print("Hi I'm Ansr. I'm the ultimate resource for ulti handbook questions. What can I help you with today?")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)
        if (bot.followup_question(bot_input)):
            # append input to valid info array
            print(bot.conversation)
            context.append(bot.fixed_queue.peek().text)
        else:
            # empty out valid info array
            context = []
        print(context)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Till next time! Goodbye.")
        break
