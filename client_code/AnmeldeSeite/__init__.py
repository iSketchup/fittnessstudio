from ._anvil_designer import AnmeldeSeiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AnmeldeSeite(AnmeldeSeiteTemplate):
  def __init__(self, KID, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = anvil.server.call('query_database_dict_Sign_Page', KID)

    # Any code you write here will run before the form opens.
