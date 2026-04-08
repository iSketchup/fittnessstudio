from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print(anvil.server.call('query_database_dict_Main_Page'))
    self.RP_All.items =  anvil.server.call('query_database_dict_Main_Page')
    
    # Any code you write here will run before the form opens.
