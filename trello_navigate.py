import requests

try:
    from trello import TrelloCommand
    from trello_cache import TrelloCache
    from operations import BoardOperation, CardOperation
except ImportError:
    from .trello import TrelloCommand
    from .trello_cache import TrelloCache
    from .operations import BoardOperation, CardOperation

class Navegable(TrelloCommand):
    def work(self, connection):
        try:
            self.safe_work(connection)
        except requests.exceptions.HTTPError as e:
            self.show_token_expired_help(e)
            raise e

    def display(self, names, callback = None):
        self.show_quick_panel(names, callback)

    def input(self, label, callback = None):
        self.show_input_panel(label, "", callback)

    def insert(self, text):
        self.insert_text(text)

    def output(self, text):
        if self.results_in_new_tab:
            self.show_in_tab(text)
        else:
            self.show_output_panel(text)

    def output_editable(self, text, extra = None):
        self.show_in_editable_tab(text, extra)

    def on_cached_operation(self, fn):
        if TrelloCache.is_empty():
            self.show_output_panel_composing("No active Trello List found.", "This command works on the last visited list using 'Trello: Navigate'.")
        else:
            operation = TrelloCache.get() 
            trello_element = operation.trello_element
            fn(operation, trello_element)

class TrelloNavigateCommand(Navegable):
    def safe_work(self, connection):
        BoardOperation(connection.me).execute(self)

class TrelloQuickCreateCardCommand(Navegable):
    def safe_work(self, connection):
        self.on_cached_operation(
            lambda operation, list: operation.get_name(label="Card name (on list %s/%s)" % (list.board.name, list.name))
        )
            
class TrelloCreateCardWithDescriptionCommand(Navegable):
    def safe_work(self, connection):
        self.on_cached_operation(
            lambda operation, list: operation.create_with_description(label="[List %s/%s]. " % (list.board.name, list.name))
        )           
