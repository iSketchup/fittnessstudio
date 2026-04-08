import sqlite3
import os

DB_NAME = "Luis_Kaufmann_fitnessstudio.db"

# Alte DB löschen falls vorhanden (für sauberen Neustart)
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# ─────────────────────────────────────────────
# 1. TABELLEN ANLEGEN
# ─────────────────────────────────────────────

cur.executescript("""
    CREATE TABLE Trainer (
        TID           INTEGER PRIMARY KEY AUTOINCREMENT,
        Vorname       TEXT    NOT NULL,
        Nachname      TEXT    NOT NULL,
        Spezialgebiet TEXT    NOT NULL
    );

    CREATE TABLE Kurse (
        KID                   INTEGER PRIMARY KEY AUTOINCREMENT,
        TID                   INTEGER NOT NULL,
        Bezeichnung           TEXT    NOT NULL,
        Wochentag             TEXT    NOT NULL,
        Uhrzeit               TEXT    NOT NULL,
        maxTeilnehmer         INTEGER NOT NULL,
        angemeldeteTeilnehmer INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (TID) REFERENCES Trainer(TID)
    );

    CREATE TABLE Mitglieder (
        MID            INTEGER PRIMARY KEY AUTOINCREMENT,
        Vorname        TEXT    NOT NULL,
        Nachname       TEXT    NOT NULL,
        Beitrittsdatum TEXT    NOT NULL,
        Email          TEXT    NOT NULL
    );

    CREATE TABLE Anmeldung (
        AID          INTEGER PRIMARY KEY AUTOINCREMENT,
        KID          INTEGER NOT NULL,
        MID          INTEGER NOT NULL,
        Anmeldedatum TEXT    NOT NULL,
        FOREIGN KEY (KID) REFERENCES Kurse(KID),
        FOREIGN KEY (MID) REFERENCES Mitglieder(MID)
    );
""")

# ─────────────────────────────────────────────
# 2. BEISPIELDATEN EINFÜGEN
# ─────────────────────────────────────────────

# 3 Trainer
trainer = [
    ("Arnold", "Schwarzenhuber", "Bodybuilding"),
    ("Yogi",   "Bär",            "Entspannung"),
    ("Usain",  "Boltens",        "Sprint-Ausdauer"),
]
cur.executemany(
    "INSERT INTO Trainer (Vorname, Nachname, Spezialgebiet) VALUES (?, ?, ?)",
    trainer
)

# 5 Kurse (TID, Bezeichnung, Wochentag, Uhrzeit, maxTeilnehmer, angemeldeteTeilnehmer)
kurse = [
    (1, "Pump it Up",          "Montag",     "18:00", 15, 3),
    (2, "Zen-Garten Yoga",     "Dienstag",   "09:00", 10, 1),
    (3, "Laufband-Massaker",   "Mittwoch",   "17:30", 20, 2),
    (1, "Bizeps-Bibel",        "Donnerstag", "19:00", 12, 1),
    (2, "Tiefenentspannung",   "Freitag",    "16:00",  8, 1),
]
cur.executemany(
    "INSERT INTO Kurse (TID, Bezeichnung, Wochentag, Uhrzeit, maxTeilnehmer, angemeldeteTeilnehmer) VALUES (?, ?, ?, ?, ?, ?)",
    kurse
)

# 6 Mitglieder
mitglieder = [
    ("Max",   "Mustermann", "2026-01-01", "max@mail.de"),
    ("Erika", "Beispiel",   "2026-01-15", "erika@web.de"),
    ("Otto",  "Normaler",   "2026-02-10", "otto@gmx.at"),
    ("Susi",  "Sorglos",    "2026-02-20", "susi@mail.com"),
    ("Kevin", "Allein",     "2026-03-05", "kevin@zuhause.de"),
    ("Anna",  "Log",        "2026-03-12", "anna@server.net"),
]
cur.executemany(
    "INSERT INTO Mitglieder (Vorname, Nachname, Beitrittsdatum, Email) VALUES (?, ?, ?, ?)",
    mitglieder
)

# 8 Anmeldungen (KID, MID, Anmeldedatum)
anmeldungen = [
    (1, 1, "2026-04-01"),   # Max   → Pump it Up
    (1, 2, "2026-04-01"),   # Erika → Pump it Up
    (2, 3, "2026-04-02"),   # Otto  → Zen-Garten Yoga
    (3, 4, "2026-04-02"),   # Susi  → Laufband-Massaker
    (4, 5, "2026-04-03"),   # Kevin → Bizeps-Bibel
    (5, 6, "2026-04-03"),   # Anna  → Tiefenentspannung
    (1, 4, "2026-04-04"),   # Susi  → Pump it Up
    (3, 1, "2026-04-04"),   # Max   → Laufband-Massaker
]
cur.executemany(
    "INSERT INTO Anmeldung (KID, MID, Anmeldedatum) VALUES (?, ?, ?)",
    anmeldungen
)

conn.commit()

# ─────────────────────────────────────────────
# 3. KONTROLLE – TABELLENINHALTE AUSGEBEN
# ─────────────────────────────────────────────

def print_table(title, query):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    print("  " + " | ".join(f"{c:<18}" for c in cols))
    print("  " + "-" * (21 * len(cols)))
    for row in cur.fetchall():
        print("  " + " | ".join(f"{str(v):<18}" for v in row))

print_table("TRAINER",    "SELECT * FROM Trainer")
print_table("KURSE",      "SELECT * FROM Kurse")
print_table("MITGLIEDER", "SELECT * FROM Mitglieder")
print_table("ANMELDUNGEN","SELECT * FROM Anmeldung")

# JOIN-Abfrage: Wer hat sich für welchen Kurs angemeldet?
print(f"\n{'─'*55}")
print("  ANMELDUNGEN (verknüpft)")
print(f"{'─'*55}")
cur.execute("""
    SELECT
        a.AID,
        m.Vorname || ' ' || m.Nachname  AS Mitglied,
        k.Bezeichnung                   AS Kurs,
        k.Wochentag,
        k.Uhrzeit,
        a.Anmeldedatum
    FROM Anmeldung a
    JOIN Mitglieder m ON a.MID = m.MID
    JOIN Kurse      k ON a.KID = k.KID
    ORDER BY a.AID
""")
cols = [d[0] for d in cur.description]
print("  " + " | ".join(f"{c:<20}" for c in cols))
print("  " + "-" * (23 * len(cols)))
for row in cur.fetchall():
    print("  " + " | ".join(f"{str(v):<20}" for v in row))

conn.close()
print(f"\n✓ Datenbank '{DB_NAME}' erfolgreich erstellt.\n")
