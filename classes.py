from db import *
from dicts import *

def print_table(rows, headers=None, max_width=30, null="–"):
  """Print a list of dicts as an aligned terminal table."""
  if not rows:
    print("(no rows)")
    return

  if headers is None:
    headers = list(rows[0].keys())

  def cell(v):
    return null if v is None else str(v)

  def pad(s, width):
    if len(s) > width:                       # truncate
      s = s[: width - 1] + "…"
      while len(s) > width:
        s = s[:-1]
    return s + " " * (width - len(s))        # pad right

  # column widths
  widths = []
  for h in headers:
    w = len(str(h))
    for r in rows:
      w = max(w, len(cell(r.get(h, ""))))
    widths.append(min(w, max_width))

  sep = "-+-".join("-" * w for w in widths)

  print(" | ".join(pad(str(h), w) for h, w in zip(headers, widths)))
  print(sep)
  for r in rows:
      print(" | ".join(pad(cell(r.get(h, "")), w) for h, w in zip(headers, widths)))

# ===== Properties ===== 
class PropertiesImprovements:
  def __init__(self):
    self.property_improvements_table = get_property_improvement()
    
  @property
  def total_properties_improvements_costs(self):
    costs = 0
    for row in self.property_improvements_table:
      costs += row['cost']
    return costs
  
  def get_costs_rows_by_id(self, property_id):
    rows = []
    for r in self.property_improvements_table:
      if r['property_id'] == property_id:
        rows.append(r)
    return rows
  
  def get_total_costs_by_id(self, property_id):
    costs = 0
    for r in self.property_improvements_table:
      if r['property_id'] == property_id:
        costs += r['cost']
    return costs

class Properties(PropertiesImprovements):
  def __init__(self):
    super().__init__()
    self.property_table = get_property()
  
  @property
  def property_table_with_cost(self):
    pwc = []
    for r in self.property_table:
      r['cost'] = self.get_total_costs_by_id(r['id'])
      pwc.append(r)
    return pwc
  
  def get_property_by_id(self, id):
    for r in self.property_table:
      if r['id'] == id:
        return r
  
  def get_property_with_cost_by_id(self, id):
    for r in self.property_table:
      if r['id'] == id:
        r['cost'] = self.get_total_costs_by_id(r['id'])
        return r
  
  @property
  def total_base(self):
    bases = 0
    for p in self.property_table:
      bases += p['buy_price']
    bases += self.total_properties_improvements_costs
    return bases
  
  def get_total_property_base_by_id(self, id):
    base = 0
    for p in self.property_table:
      if p['id'] == id:
        base = p['buy_price'] + self.get_total_costs_by_id(id)
    return base
  
  def is_property_sold(self, id):
    for r in self.property_table:
      if r['id'] == id:
        return bool(r['sell_price'])
      
  @property
  def total_profit(self):
    profit = 0
    for p in self.property_table:
      if self.is_property_sold(p['id']):
        profit += p['sell_price'] - self.get_total_property_base_by_id(p['id'])
    return profit
  
  def property_html_dict(self, data=True):
    if len(self.property_table) <= 0:
      if len(self.property_table) == 0:
        content = 'خطأ: لاتوجد عقارات بعد.'
      else:
        content = 'خطأ: مشكلة في عدد العقارات.'
      return {
        'status': 'error',
        'content': content,
        'name': 'عقارات',
        'url': '/property',
        'base': 0,
        'profit': 0,
      }
    else:
      return {
        'status': 'success',
        'content': self.property_table_with_cost if data else None,
        'name': 'عقارات',
        'url': '/property',
        'base': self.total_base,
        'profit': self.total_profit,
      }

# ===== Customers ===== 
class CustomerRecord:
  def __init__(self):
    self.customer_record_table = get_customer_record()
  
  def get_customer_records_by_id(self, customer_id):
    records = []
    for r in self.customer_record_table:
      if r['customer_id'] == customer_id:
        records.append(r)
    return records
  
  @property
  def is_customer_record(self, id):
    for r in self.customer_record_table():
      if r[id] == id:
        return True
    return False
  
  @property
  def get_total_balance(self):
    for_us = 0
    for_them = 0
    for r in self.customer_record_table:
      if r['amount'] <= 0:
        for_us += r['amount']
      else:
        for_them += r['amount']
    
    return {
      "for_us": for_us,
      "for_them": for_them
    }
  
  def get_total_customer_balance_by_id(self, customer_id):
    for_us = 0
    for_them = 0
    for r in self.customer_record_table:
      if r['customer_id'] == customer_id:
        if r['amount'] <= 0:
          for_us += r['amount']
        else:
          for_them += r['amount']
    
    return {
      "for_us": for_us,
      "for_them": for_them
    }
  
class Customers(CustomerRecord):
  def __init__(self):
    super().__init__()
    self.customer_table = get_customer()
  
  @property
  def get_customer_table_with_balance(self):
    customers = self.customer_table
    for c in customers:
      c['balance'] = self.get_total_customer_balance_by_id(c['id'])
    return customers
  
  def get_customer_by_id_with_balance(self, id):
    customers = self.customer_table
    for c in customers:
      if c['id'] == id:
        c['balance'] = self.get_total_customer_balance_by_id(c['id'])
        return c
  
  def customer_html_dict(self, data=True):
    if len(self.customer_table) <= 0 :
      if len(self.customer_table) == 0:
        content = 'خطأ: لايوجد زبائن بعد.'
      else:
        content = 'خطأ: مشكلة في عدد الزبائن.'
      return {
        'status': 'error',
        'content': content,
        'name': 'الزبائن',
        'url': '/customer',
        'for_us': 0,
        'for_them': 0,
      }
    else:
      balance = self.get_total_balance
      return {
        'status': 'success',
        'content': self.get_customer_table_with_balance if data else None,
        'name': 'الزبائن',
        'url': '/customer',
        'for_us': balance['for_us'],
        'for_them': balance['for_them'],
      }

# ===== Crops =====    
class CropCosts:
  def __init__(self):
    self.crop_costs_table = get_crop_costs()


class CropSale():
  def __init__(self):
    self.crop_costs_table = get_crop_costs()

class CropLot(CropSale, CropCosts):
  def __init__(self):
    super().__init__()
    self.crop_lot = get_crop_lot()

class Crop(CropLot):
  def __init__(self):
    super().__init__()
    self.crop_table = get_crop()
  
  
  @property
  def total_base():
    pass
    
    
  def crop_html_dict(self, data=True):
    if len(self.crop_table) <= 0:
      if len(self.crop_table) == 0:
        content = 'خطأ: لاتوجد محاصيل بعد.'
      else:
        content = 'خطأ: مشكلة في عدد المحاصيل.'
      return {
        'status': 'error',
        'content': content,
        'name': 'محاصيل',
        'url': '/crop',
        'base': 0,
        'profit': 0
      }
    else:
      data_test = [
        {"name": "حنطة"}
      ]
      return {
        'status': 'success',
        # 'content': self.property_table_with_cost if data else None,
        'content': data_test,
        'name': 'محاصيل',
        'url': '/crop',
        # 'base': self.total_base,
        'base': 10000,
        # 'profit': self.total_profit,
        'profit': 5000,
      }

    
  
# print(Crop().crop_html_dict()['base'])












































# ===== Customers ===== 
class Trades(Properties, Customers, Crop):
  def __init__(self):
    Properties.__init__(self)
    Customers.__init__(self)
    Crop.__init__(self)
  
  @property
  def trades_html_dict(self):
    content = [
      get_truck_dict(),
      get_mixer_dict(),
      get_block_factory_dict(),
      self.property_html_dict(data=False),
      self.customer_html_dict(data=False),
      self.crop_html_dict(data=False),
      get_projects_dict()
    ]
    total_base = 0
    total_profit = 0
    for t in content:
      if not t['status'] == 'error':
        if t['url'] != '/customer':
          total_base += t['base']
          total_profit += t['profit']
        else:
          total_base -= t['for_us'] + t['for_them']
        
    return {
      "content": content,
      "total_base": total_base,
      "total_profit": total_profit
    }