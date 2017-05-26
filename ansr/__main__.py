from chatterbot import ChatBot
from chatterbot.logic.best_match import BestMatch

context = [] # passed to ML Engine
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.TimeLogicAdapter',
        #ML Adapter
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter", #
    database="../database.db",
    read_only=True,
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

bot.storage.drop()
bot.train("chatterbot.corpus.english.ansr")
bot.train("chatterbot.corpus.english.greetings")

print("Hi I'm Ansr. I'm the ultimate resource for ulti handbook questions. What can I help you with today?")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)
        if (bot.followup_question(bot_input)):
            # append input to valid info array
            # print(bot.conversation)
            context.append(bot.fixed_queue.peek().text)
        else:
            # empty out valid info array
            context = []
        print(context)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Till next time! Goodbye.")
        break
