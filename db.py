import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

def new_db():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  # truck table
      # id             INTEGER PRIMARY KEY AUTOINCREMENT,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS truck (
      name           TEXT NOT NULL,
      purchase_price REAL NOT NULL,
      notes          TEXT
    );       
  ''')
  # truck_profit table
      # truck_id  INTEGER NOT NULL,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS truck_profit (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      month_year     TEXT NOT NULL,
      amount    REAL NOT NULL,
      notes     TEXT
    );       
  ''')
  # mixer table
      # id             INTEGER PRIMARY KEY AUTOINCREMENT,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS mixer (
      name           TEXT NOT NULL,
      purchase_price REAL NOT NULL,
      notes          TEXT
    );       
  ''')
  # mixer_profit table
      # mixer_id  INTEGER NOT NULL,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS mixer_profit (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      month_year     TEXT NOT NULL,
      amount    REAL NOT NULL,
      notes     TEXT
    );       
  ''')
  # block_factory table
      # id             INTEGER PRIMARY KEY AUTOINCREMENT,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS block_factory (
      name           TEXT NOT NULL,
      purchase_price REAL NOT NULL,
      notes          TEXT
    );       
  ''')
  # block_factory_profit table
      # factory_id  INTEGER NOT NULL,
  cur.execute('''
    CREATE TABLE IF NOT EXISTS block_factory_profit (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      month_year       TEXT NOT NULL,
      amount      REAL NOT NULL,
      notes       TEXT
    );       
  ''')
  # block_factory_expense table
  # cur.execute('''
  #   CREATE TABLE IF NOT EXISTS block_factory_expense (
  #     id           INTEGER PRIMARY KEY AUTOINCREMENT,
  #     factory_id   INTEGER NOT NULL,
  #     description  TEXT NOT NULL,
  #     amount       REAL NOT NULL,
  #     expense_date TEXT NOT NULL,
  #     notes        TEXT
  #   );       
  # ''')
  # property table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS property (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      discreption TEXT NOT NULL,
      address     TEXT NOT NULL,
      buy_price   REAL NOT NULL,
      sell_price  REAL,
      seller_name TEXT NOT NULL,          -- old owner
      buyer_name  TEXT,                   -- new owner (empty until sold)
      buy_date    TEXT,
      sell_date   TEXT,
      longitude   REAL,
      latitude    REAL,
      notes       TEXT
    );      
  ''')
  # property_improvement table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS property_improvement (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      property_id   INTEGER NOT NULL,
      improve_date  TEXT,
      description   TEXT NOT NULL,
      cost          REAL NOT NULL,
      notes         TEXT
    );       
  ''')
  # customer table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS customer (
      id    INTEGER PRIMARY KEY AUTOINCREMENT,
      name  TEXT NOT NULL,
      notes TEXT
    );       
  ''')
  # customer_record table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS customer_record (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      customer_id  INTEGER NOT NULL,
      amount       REAL NOT NULL,
      record_date  TEXT NOT NULL,
      notes        TEXT
    );       
  ''')
  # crop table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS crop (
      id   INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE
    );       
  ''')
  # crop_lot table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS crop_lot (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      crop_id          INTEGER NOT NULL,
      buy_date         TEXT,
      weight_kg        REAL NOT NULL,
      price_per_kg     REAL NOT NULL,
      storage_location_address TEXT,
      notes            TEXT
    );       
  ''')
  # crop_sale table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS crop_sale (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      lot_id        INTEGER NOT NULL,
      sale_date     TEXT,
      weight_kg     REAL NOT NULL,
      price_per_kg  REAL NOT NULL,
      buyer_name    TEXT,
      notes         TEXT
    );       
  ''')
  # crop_costs table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS crop_costs (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      lot_id        INTEGER NOT NULL,
      cost_name     TEXT,
      cost_date     TEXT,
      price  REAL NOT NULL,
      notes         TEXT
    );       
  ''')
  # project table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS project (
      id    INTEGER PRIMARY KEY AUTOINCREMENT,
      name  TEXT NOT NULL,
      notes TEXT
    );       
  ''')
  # project_item table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS project_item (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      project_id  INTEGER NOT NULL,
      name        TEXT NOT NULL
    );       
  ''')
  # project_item_record table
  cur.execute('''
    CREATE TABLE IF NOT EXISTS project_item_record (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id      INTEGER NOT NULL,
      record_date  TEXT NOT NULL,
      quantity     REAL NOT NULL,
      unit         TEXT,
      unit_price   REAL NOT NULL,
      supplier     TEXT,
      notes        TEXT
    );       
  ''')
  # add truck
  conn.commit()
  conn.close()
 
 
 # truck table

# truck table
def get_truck():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM truck').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_truck():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM truck').fetchall())
  conn.close()
  return sts

# truck_profit table
def get_truck_profit():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM truck_profit').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_truck_profit_reecord(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM truck_profit WHERE id=?', (id,)).fetchall())
  conn.close()
  return sts

# mixer table
def get_mixer():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM mixer').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_mixer():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM mixer').fetchall())
  conn.close()
  return sts

# mixer_profit table
def get_mixer_profit():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM mixer_profit').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_mixer_profit_reecord(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM mixer_profit WHERE id=?', (id,)).fetchall())
  conn.close()
  return sts

# block_factory table
def get_block_factory():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM block_factory').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_block_factory():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM block_factory').fetchall())
  conn.close()
  return sts

# block_factory_profit table
def get_block_factory_profit():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM block_factory_profit').fetchall()
  conn.close()
  return [dict(r) for r in rows]

def is_block_factory_profit_reecord(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM block_factory_profit WHERE id=?', (id,)).fetchall())
  conn.close()
  return sts

# property table
def get_property(id=None):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  if id:
    rows = cur.execute('SELECT * FROM property WHERE id=?', (id,)).fetchone()
  else:
    rows = cur.execute('SELECT * FROM property').fetchall()
  conn.close()
  return [dict(r) for r in rows]


def is_property(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM property WHERE id=?', (id,)).fetchall())
  conn.close()
  return sts

# property_improvement table
def get_property_improvement(id=None):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = []
  if id:
    rows = cur.execute('SELECT * FROM property_improvement WHERE property_id=?', (id,)).fetchall()
  else:
    rows = cur.execute('SELECT * FROM property_improvement').fetchall()
  conn.close()
  return rows

def is_property_has_improvement(property_id):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM property_improvement  WHERE property_id=?', (property_id,)).fetchone())
  conn.close()
  return sts

def is_improvement(improvement_id):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  sts = bool(cur.execute('SELECT * FROM property_improvement  WHERE id=?', (improvement_id,)).fetchone())
  conn.close()
  return sts

# customer table
def get_customer():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM customer').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# customer_record table
def get_customer_record():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM customer_record').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# crop table
def get_crop():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM crop').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# crop_lot table
def get_crop_lot():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM crop_lot').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# crop_sale table
def get_crop_sale():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM crop_sale').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# crop_costs table
def get_crop_costs():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM crop_costs').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# project table
def get_project():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM project').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# project_item table
def get_project_item():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM project_item').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# project_item_record table
def get_project_item_record():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  rows = cur.execute('SELECT * FROM project_item_record').fetchall()
  conn.close()
  return [dict(r) for r in rows]

# all_db table
def get_all_db():
  return {
    'truck': get_truck(),
    'truck_profit': get_truck_profit(),
    'mixer': get_mixer(),
    'mixer_profit': get_mixer_profit(),
    'block_factory': get_block_factory(),
    'block_factory_profit': get_block_factory_profit(),
    # 'block_factory_expense': get_block_factory_expense(),
    'property': get_property(),
    'property_improvement': get_property_improvement(),
    'customer': get_customer(),
    'customer_record': get_customer_record(),
    'crop': get_crop(), 'crop_lot': get_crop_lot(),
    'crop_sale': get_crop_sale(),
    'crop_costs': get_crop_costs(),
    'project': get_project(),
    'project_item': get_project_item(),
    'project_item_record': get_project_item_record()
  }


