from __future__ import unicode_literals
import warnings
from collections import Counter
from chatterbot import utils
from .logic_adapter import LogicAdapter


class MultiLogicAdapter(LogicAdapter):
    """
    MultiLogicAdapter allows ChatterBot to use multiple logic
    adapters. It has methods that allow ChatterBot to add an
    adapter, set the chat bot, and process an input statement
    to get a response.
    """

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        # Logic adapters added by the chat bot
        self.adapters = []

        # Requied logic adapters that must always be present
        self.system_adapters = []

    def process(self, statement):
        """
        Returns the outout of a selection of logic adapters
        for a given input statement.

        :param statement: The input statement to be processed.
        """
        results = []
        result = None
        max_confidence = -1

        for adapter in self.get_adapters():
            # Check what adapters are processing
            # EDIT removed can_process flag
            if True: # adapter.can_process(statement):
                print(adapter)
                output = adapter.process(statement)

                if(adapter != self.get_adapters()[0]):
                    if(output.confidence > .3):
                        output.confidence = .3

                if type(output) == tuple:
                    warnings.warn(
                        '{} returned two values when just a Statement object was expected. '
                        'You should update your logic adapter to return just the Statement object. '
                        'Make sure that statement.confidence is being set.'.format(adapter.class_name),
                        DeprecationWarning
                    )
                    output = output[1]

                results.append((output.confidence, output, ))

                self.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        adapter.class_name, output.text, output.confidence
                    )
                )

                print("Confidence: %f \t MaxConf: %f \t Output: %s" % (output.confidence, max_confidence, output))

                if output.confidence > max_confidence:
                    result = output
                    max_confidence = output.confidence
            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
                )
        # If multiple adapters agree on the same statement,
        # then that statement is more likely to be the correct response
        # EDIT: reduced length to 1
        # if len(results) > 1:
        #     statements = [s[1] for s in results]
        #     count = Counter(statements)
        #     most_common = count.most_common()
        #     print(results)
        #     if most_common[0][1] > 1:
        #         # print(most_common[0])
        #         result = most_common[0][0]
        #         max_confidence = self.get_greatest_confidence(result, results)

        result.confidence = max_confidence
        return result

    def get_greatest_confidence(self, statement, options):
        """
        Returns the greatest confidence value for a statement that occurs
        multiple times in the set of options.

        :param statement: A statement object.
        :param options: A tuple in the format of (confidence, statement).
        """
        print("Checking greating confid...")
        values = []
        for option in options:
            if option[1] == statement:
                values.append(option[0])
                print(option[0])

        return max(values)

    def get_adapters(self):
        """
        Return a list of all logic adapters being used, including system logic adapters.
        """
        adapters = []
        adapters.extend(self.adapters)
        adapters.extend(self.system_adapters)
        return adapters

    def add_adapter(self, adapter, **kwargs):
        """
        Appends a logic adapter to the list of logic adapters being used.

        :param adapter: The logic adapter to be added.
        :type adapter: `LogicAdapter`
        """
        utils.validate_adapter_class(adapter, LogicAdapter)
        adapter = utils.initialize_class(adapter, **kwargs)
        self.adapters.append(adapter)

    def insert_logic_adapter(self, logic_adapter, insert_index, **kwargs):
        """
        Adds a logic adapter at a specified index.

        :param logic_adapter: The string path to the logic adapter to add.
        :type logic_adapter: str

        :param insert_index: The index to insert the logic adapter into the list at.
        :type insert_index: int
        """
        utils.validate_adapter_class(logic_adapter, LogicAdapter)

        NewAdapter = utils.import_module(logic_adapter)
        adapter = NewAdapter(**kwargs)

        self.adapters.insert(insert_index, adapter)

    def remove_logic_adapter(self, adapter_name):
        """
        Removes a logic adapter from the chat bot.

        :param adapter_name: The class name of the adapter to remove.
        :type adapter_name: str
        """
        for index, adapter in enumerate(self.adapters):
            if adapter_name == type(adapter).__name__:
                del self.adapters[index]
                return True
        return False

    def set_chatbot(self, chatbot):
        """
        Set the chatbot for each of the contained logic adapters.
        """
        super(MultiLogicAdapter, self).set_chatbot(chatbot)

        for adapter in self.get_adapters():
            adapter.set_chatbot(chatbot)