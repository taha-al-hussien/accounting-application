import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

# Truck
def post_truck_config(truck):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO truck (name, purchase_price, notes) VALUES (?,?,?)', (truck['name'], truck['purchase_price'],  truck.get('notes', '')))
  conn.commit()
  conn.close()

def post_truck_edit(truck):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE truck SET purchase_price = ?', (truck['purchase_price'],))
  conn.commit()
  conn.close()

def add_truck_profit(profit):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO truck_profit (month_year, amount, notes) VALUES (?,?,?)', (profit['month_year'], profit['amount'],  profit.get('notes', '')))
  conn.commit()
  conn.close()

def edit_truck_profit(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE truck_profit SET month_year = ?, amount = ?, notes = ? WHERE id = ?', (record['month_year'], record['amount'], record.get('notes', ''), record['id']))
  conn.commit()
  conn.close()

def delete_truck_profit(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM truck_profit WHERE id=?', (id,))
  conn.commit()
  conn.close()
  
def delete_truck_profit_all():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM truck_profit')
  conn.commit()
  conn.close()

# Mixer
def post_mixer_config(mixer):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO mixer (name, purchase_price, notes) VALUES (?,?,?)', (mixer['name'], mixer['purchase_price'],  mixer.get('notes', '')))
  conn.commit()
  conn.close()

def post_mixer_edit(mixer):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE mixer SET purchase_price = ?', (mixer['purchase_price'],))
  conn.commit()
  conn.close()

def add_mixer_profit(profit):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO mixer_profit (month_year, amount, notes) VALUES (?,?,?)', (profit['month_year'], profit['amount'],  profit.get('notes', '')))
  conn.commit()
  conn.close()

def edit_mixer_profit(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE mixer_profit SET month_year = ?, amount = ?, notes = ? WHERE id = ?', (record['month_year'], record['amount'], record.get('notes', ''), record['id']))
  conn.commit()
  conn.close()

def delete_mixer_profit(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM mixer_profit WHERE id=?', (id,))
  conn.commit()
  conn.close()

def delete_mixer_profit_all():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM mixer_profit')
  conn.commit()
  conn.close()

# Block factory
def post_block_factory_config(block_factory):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO block_factory (name, purchase_price, notes) VALUES (?,?,?)', (block_factory['name'], block_factory['purchase_price'],  block_factory.get('notes', '')))
  conn.commit()
  conn.close()

def post_block_factory_edit(block_factory):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE block_factory SET purchase_price = ?', (block_factory['purchase_price'],))
  conn.commit()
  conn.close()

def add_block_factory_profit(profit):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('INSERT INTO block_factory_profit (month_year, amount, notes) VALUES (?,?,?)', (profit['month_year'], profit['amount'],  profit.get('notes', '')))
  conn.commit()
  conn.close()

def edit_block_factory_profit(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE block_factory_profit SET month_year = ?, amount = ?, notes = ? WHERE id = ?', (record['month_year'], record['amount'], record.get('notes', ''), record['id']))
  conn.commit()
  conn.close()

def delete_block_factory_profit(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM block_factory_profit WHERE id=?', (id,))
  conn.commit()
  conn.close()
  
def delete_block_factory_profit_all():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM block_factory_profit')
  conn.commit()
  conn.close()

def add_property(property):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    INSERT INTO property (
      discreption,
      address,
      buy_price,
      seller_name,
      buy_date,
      longitude,
      latitude,
      notes
    ) VALUES (?,?,?,?,?,?,?,?)
    ''',
    (
      property.get("discreption", None),
      property.get("address", None),
      property.get("buy_price", None),
      property.get("seller_name", None),
      property.get("buy_date", None),
      property.get("longitude", None),
      property.get("latitude", None),
      property.get("notes", None)
    )
  )
  conn.commit()
  conn.close()
  
def edit_property(property):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    UPDATE property SET 
      discreption = ?,
      address = ?,
      buy_price = ?,
      seller_name = ?,
      sell_price = ?,
      buyer_name = ?,
      buy_date = ?,
      longitude = ?,
      latitude = ?,
      notes = ?
      WHERE id = ?
    ''',
    (
      property["discreption"],
      property["address"],
      property["buy_price"],
      property["seller_name"],
      property.get("sell_price", None),
      property.get("buyer_name", None),
      property["buy_date"],
      property["longitude"],
      property["latitude"],
      property["notes"],
      property["id"]
      
    )
  )
  conn.commit()
  conn.close()

# def edit_property(record):
#   conn = sqlite3.connect(DB_PATH)
#   cur = conn.cursor()
#   cur.execute('UPDATE property SET month_year = ?, amount = ?, notes = ? WHERE id = ?', (record['month_year'], record['amount'], record.get('notes', ''), record['id']))
#   conn.commit()
#   conn.close()

def delete_property(id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM property WHERE id=?', (id,))
  conn.commit()
  conn.close()
  delete_property_improvements(id)
  
def sell_property(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('UPDATE property SET buyer_name = ?, sell_price = ?, sell_date = ? WHERE id = ?', (record['buyer_name'], record['sell_price'], record['sell_date'], record['id']))
  conn.commit()
  conn.close()
  
def add_property_improvements(property_improvements):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    INSERT INTO property_improvement (
      description,
      cost,
      improve_date,
      property_id,
      notes
    ) VALUES (?,?,?,?,?)
    ''',
    (
      property_improvements.get("description", None),
      property_improvements.get("cost", None),
      property_improvements.get("improve_date", None),
      property_improvements.get("property_id", None),
      property_improvements.get("notes", None),
    )
  )
  conn.commit()
  conn.close()
  
def delete_property_improvement(improvement_id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM property_improvement WHERE id=?', (improvement_id,))
  conn.commit()
  conn.close()
  
def delete_property_improvements(property_id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM property_improvement WHERE property_id=?', (property_id,))
  conn.commit()
  conn.close()
  
def edit_property_improvements(property_improvements):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    UPDATE property_improvement  SET
      description = ?,
      cost = ?,
      improve_date = ?,
      property_id = ?,
      notes = ?
      WHERE id = ?
    ''',
    (
      property_improvements["description"],
      property_improvements["cost"],
      property_improvements["improve_date"],
      property_improvements["property_id"],
      property_improvements["notes"],
      property_improvements["id"]
    )
  )
  conn.commit()
  conn.close()
  
def add_customer(customer):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    INSERT INTO customer (
      name,
      notes
    ) VALUES (?,?)
    ''',
    (
      customer.get("name"),
      customer.get("notes", None),
    )
  )
  conn.commit()
  conn.close()

def edit_customer(customer):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    UPDATE customer  SET
      name = ?,
      notes = ?
      WHERE id = ?
    ''',
    (
      customer["name"],
      customer["notes"],
      customer["id"]
    )
  )
  conn.commit()
  conn.close()
  
def delete_customer(customer_id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM customer WHERE id=?', (customer_id,))
  conn.commit()
  conn.close()
  
def delete_customers():
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM customer')
  cur.execute('DELETE FROM customer_record')
  conn.commit()
  conn.close()
  
def add_customer_record(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    INSERT INTO customer_record (
      customer_id,
      amount,
      record_date,
      notes
    ) VALUES (?,?,?,?)
    ''',
    (
      record.get("customer_id"),
      record.get("amount"),
      record.get("record_date"),
      record.get("notes", None),
    )
  )
  conn.commit()
  conn.close()
  
def edit_customer_record(record):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('''
    UPDATE customer_record  SET
      amount = ?,
      record_date = ?,
      notes = ?
      WHERE id = ?
    ''',
    (
      record["amount"],
      record["record_date"],
      record["notes"],
      record["id"]
    )
  )
  conn.commit()
  conn.close()
  
def delete_customer_record(record_id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM customer_record WHERE id=?', (record_id,))
  conn.commit()
  conn.close()
  
def delete_customer_records(customer_id):
  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()
  cur.execute('DELETE FROM customer_record WHERE customer_id=?', (customer_id,))
  conn.commit()
  conn.close()
  
  
  