import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database_dict_Main_Page():
  # Wir starten bei Kurse und holen uns nur den Trainer dazu
  query = '''SELECT 
    K.KID,
    K.Bezeichnung, 
    K.Wochentag, 
    K.Uhrzeit, 
    T.Vorname || ' ' || T.Nachname AS Trainer,
    (SELECT COUNT(*) FROM Anmeldung A WHERE A.KID = K.KID) || '/' || K.maxTeilnehmer AS Teilnehmer
FROM Kurse K
JOIN Trainer T ON K.TID = T.TID;
  '''
  with sqlite3.connect(data_files["Luis_Kaufmann_Fitnessstudio.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]


@anvil.server.callable
def query_database_dict_Sign_Page(KID):
  # Wir starten bei Kurse und holen uns nur den Trainer dazu
  query = '''Select
  Vorname || ' ' || M.Nachname AS Mitglied
  From Mitglieder M
  '''
  with sqlite3.connect(data_files["Luis_Kaufmann_Fitnessstudio.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def add_anmeldung(mid, kid):
  # Wir nehmen das aktuelle Datum für die Anmeldung
  import datetime
  heute = datetime.date.today().strftime("%d.%m.%Y")

  query = f'''
    INSERT INTO Anmeldung ({kid}, {mid}, {heute})
    VALUES (?, ?, ?)
    '''

  # Verbindung zur Datenbank
  with sqlite3.connect(data_files["Luis_Kaufmann_Fitnessstudio.db"]) as conn:
    cur = conn.cursor()
    # Den Befehl ausführen
    cur.execute(query, (kid, mid, heute))
    # Wichtig: Speichern!
    conn.commit()

  return True