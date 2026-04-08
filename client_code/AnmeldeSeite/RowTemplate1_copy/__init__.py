from ._anvil_designer import RowTemplate1_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.js.window import jQuery


class RowTemplate1_copy(RowTemplate1_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.form_show()

  def form_show(self, **event_args):
    """Wird aufgerufen, wenn die Zeile angezeigt wird"""
    # Registriert den Klick auf die gesamte Zeilefrom anvil.js.window import jQuery

    node = anvil.js.get_dom_node(self)

    jQuery(node).css(
      {"cursor": "pointer", "transition": "background-color 0.2s ease"}
    ).on("click", self.row_click).hover(
      lambda e: jQuery(node).css(
        "background-color", f"{app.theme_colors['Surface Variant']}"
      ),
      lambda e: jQuery(node).css("background-color", ""),
    )

  def row_click(self, js_event):
    anvil.server.call('add_anmeldung',self.item['MID'], self.item['KID'])
    open_form("Main")
