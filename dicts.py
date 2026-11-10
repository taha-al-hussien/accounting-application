from db import *

def get_truck_dict():
  truck_rows = get_truck()
  if len(truck_rows) != 1:
    if len(truck_rows) > 1:
      content = 'خطأ: لا يمكن وجود أكثر من قاطرة.'
    elif len(truck_rows) == 0:
      content = 'خطأ: لم تُهيّئ القاطرة بعد.'
    elif truck_rows[0]['purchase_price'] == 0.0:
      content = 'خطأ: لم تُهيّئ القاطرة بعد.'
    else:
      content = 'خطأ: مشكلة في عدد القاطرات.'
    return {
      'status': 'error',
      'content': content,
      'name': 'القاطرة',
      'url': 'truck',
      'base': 0,
      'profit': 0,
    }
  else:
    rows = get_truck_profit()
    return {
      'status': 'success',
      'content': rows,
      'name': 'القاطرة',
      'url': '/truck',
      'base': truck_rows[0]['purchase_price'],
      'profit': sum(row['amount'] for row in rows),
    }

def get_mixer_dict():
  mixer_rows = get_mixer()
  if len(mixer_rows) != 1:
    if len(mixer_rows) > 1:
      content = 'خطأ: لا يمكن وجود أكثر من جبّالة.'
    elif len(mixer_rows) == 0:
      content = 'خطأ: لم تُهيّئ الجبّالة بعد.'
    elif mixer_rows[0]['purchase_price'] == 0.0:
      content = 'خطأ: لم تُهيّئ الجبّالة بعد.'
    else:
      content = 'خطأ: مشكلة في عدد الجبّالات.'
    return {
      'status': 'error',
      'content': content,
      'name': 'الجبّالة',
      'url': 'mixer',
      'base': 0,
      'profit': 0,
    }
  else:
    rows = get_mixer_profit()
    return {
      'status': 'success',
      'content': rows,
      'name': 'الجبّالة',
      'url': '/mixer',
      'base': mixer_rows[0]['purchase_price'],
      'profit': sum(row['amount'] for row in rows),
    }

def get_block_factory_dict():
  block_factory_rows = get_block_factory()
  if len(block_factory_rows) != 1:
    if len(block_factory_rows) > 1:
      content = 'خطأ: لا يمكن وجود أكثر من معمل بلوك.'
    elif len(block_factory_rows) == 0:
      content = 'خطأ: لم يُهيّئ معمل البلوك بعد.'
    elif block_factory_rows[0]['purchase_price'] == 0.0:
      content = 'خطأ: لم يُهيّئ معمل البلوك بعد.'
    else:
      content = 'خطأ: مشكلة في عدد معامل البلوك.'
    return {
      'status': 'error',
      'content': content,
      'name': 'معمل البلوك',
      'url': 'block_factory',
      'base': 0,
      'profit': 0,
    }
  else:
    rows = get_block_factory_profit()
    return {
      'status': 'success',
      'content': rows,
      'name': 'معمل البلوك',
      'url': '/block_factory',
      'base': block_factory_rows[0]['purchase_price'],
      'profit': sum(row['amount'] for row in rows),
    }
    
def get_property_dict():
  property_rows = get_property()
  if len(property_rows) <= 0:
    if len(property_rows) == 0:
      content = 'خطأ: لاتوجد عقارات بعد.'
    else:
      content = 'خطأ: مشكلة في عدد العقارات.'
    return {
      'status': 'error',
      'content': content,
      'name': 'عقارات',
      'url': 'property',
      'base': 0,
      'profit': 0,
    }
  else:
    rows = list(get_property())
    for i in range(len(rows)):
      row = dict(rows[i])
      row['cost'] = get_property_item_dict(row['id'])['costs']
      rows[i] = row
    return {
      'status': 'success',
      'content': rows,
      'name': 'عقارات',
      'url': '/property',
      'base': sum(row['buy_price'] for row in rows) + sum(r['cost'] for r in get_property_improvement()),
      'profit': sum((((((row["sell_price"] or 0) - (row['cost'] or 0) or row['buy_price']) - row['buy_price']) or 0)) or 0 for row in rows),
    }

def get_property_item_dict(id):
  rows = get_property_improvement(id)
  return {
    'content': rows,
    'costs': sum(row['cost'] or 0 for row in rows),
  }

def get_property_item_improvement_dict(id):
  rows = get_property_improvement(id)
  return {
    'content': rows,
    'costs': sum(row['cost'] or 0 for row in rows),
  }
    
  

def get_customer_dict():
  customer_record_rows = get_customer_record()
  if len(customer_record_rows) <= 0:
    if len(customer_record_rows) == 0:
      content = 'خطأ: لاتوجد حسابات زبائن بعد.'
    else:
      content = 'خطأ: مشكلة في عدد حسابات الزبائن.'
    return {
      'status': 'error',
      'content': content,
      'name': 'حسابات الزبائن',
      'url': 'customer',
      'base': 0,
      'profit': 0,
    }
  else:
    customer_for_us = 0
    customer_for_them = 0
    for record in customer_record_rows:
      value = record['amount']
      if value < 0:
        customer_for_us += value
      else:
        customer_for_them += value
    return {
      'status': 'success',
      'name': 'حسابات الزبائن',
      'url': '/customer',
      'base': customer_for_us,
      'profit': customer_for_them,
    }
    
def get_crop_dict():
  customer_record_rows = get_crop()
  if len(customer_record_rows) <= 0:
    if len(customer_record_rows) == 0:
      content = 'خطأ: لاتوجد محاصيل بعد.'
    else:
      content = 'خطأ: مشكلة في عدد المحاصيل.'
    return {
      'status': 'error',
      'content': content,
      'name': 'محاصيل',
      'url': '/crop',
      'base': 0,
      'profit': 0,
    }
  else:
    customer_for_us = 0
    customer_for_them = 0
    for record in customer_record_rows:
      value = record['amount']
      if value < 0:
        customer_for_us += value
      else:
        customer_for_them += value
    return {
      'status': 'success',
      'name': 'محاصيل',
      'url': '/crop',
      'base': customer_for_us,
      'profit': customer_for_them,
    }

def get_projects_dict():
  customer_record_rows = get_crop()
  if len(customer_record_rows) <= 0:
    if len(customer_record_rows) == 0:
      content = 'خطأ: لاتوجد تعهدات بعد.'
    else:
      content = 'خطأ: مشكلة في عدد التعهدات.'
    return {
      'status': 'error',
      'content': content,
      'name': 'تعهدات',
      'url': '/projects',
      'base': 0,
      'profit': 0,
    }
  else:
    customer_for_us = 0
    customer_for_them = 0
    for record in customer_record_rows:
      value = record['amount']
      if value < 0:
        customer_for_us += value
      else:
        customer_for_them += value
    return {
      'status': 'success',
      'name': 'محاصيل',
      'url': '/projects',
      'base': customer_for_us,
      'profit': customer_for_them,
    }
    



# def get_trades_list():
#   return [
#     get_truck_dict(),
#     get_mixer_dict(),
#     get_block_factory_dict(),
#     Properties().property_html_dict,
#     get_customer_dict(),
#     get_crop_dict(),
#     get_projects_dict()
#   ]
      
