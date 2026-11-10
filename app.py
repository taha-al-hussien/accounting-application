from flask import Flask, render_template, request, redirect, flash
from dicts import *
from db_write import *
from classes import *
import json
app = Flask(__name__)
app.secret_key = "wooooooohoooooo"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
# Context
@app.context_processor
def inject_db():
  
  return {
    "trades": Trades().trades_html_dict,
    "company_name": "شركة طه للتجارة",
    "truck": get_truck_dict(),
    "mixer": get_mixer_dict(),
    "block_factory": get_block_factory_dict(),
  }

# 404
@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html", error=error)

# Root
@app.route('/')
def root():
  return render_template('dashbord.html', title='شركة عمار للتجارة')

# Truck
@app.route('/truck')
def truck():
  return render_template('truck.html', title='القاطرة - السجل', truck=get_truck_dict())

@app.route('/truck/config', methods=["POST"])
def truck_config():
  args = dict(request.form)
  try:
    args["purchase_price"] = int(args['purchase_price'])
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء القاطرة قيمته غير صحيحة"}), "error")
    return redirect("/truck")
  if not args.get('name', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون الاسم فارغا"}), "error")
    return redirect("/truck")
  if is_truck():
    flash(json.dumps({"msg": "خطأ: تمت اضافة القاطرة مسبقا"}), "error")
    return redirect("/truck")
  post_truck_config(args)
  flash(json.dumps({"msg": "أُضيفت القاطرة"}), "success")
  return redirect("/truck")

@app.route('/truck/edit', methods=["POST"])
def truck_edit():
  args = dict(request.form)
  try:
    args["purchase_price"] = float(args['purchase_price'])
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء القاطرة قيمته غير صحيحة"}), "error")
    return redirect("/truck")
  if not is_truck():
    flash(json.dumps({"msg": "خطأ: لا توجد شاحنة بعد"}), "error")
    return redirect("/truck")
  post_truck_edit(args)
  flash(json.dumps({"msg": "عُدلت القاطرة"}), "success")
  return redirect("/truck")

@app.route('/truck/records/add', methods=["POST"])
def truck_record_add():
  args = dict(request.form)
  if not is_truck():
    flash(json.dumps({"msg": "خطأ: لا توجد شاحنة بعد"}), "error")
    return redirect("/truck")
  try:
    args["amount"] = int(args['amount'])
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/truck")
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/truck")
  add_truck_profit(args)
  flash(json.dumps({"msg": "أُضيفت الأرباح"}), "success")
  return redirect("/truck")

@app.route('/truck/records/<int:id>/edit', methods=["POST"])
def truck_record_edit(id):
  args = dict(request.form)
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/truck")
  
  if not is_truck_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/truck")
  args['id'] = id
  try:
    args["amount"] = int(float(args['amount']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/truck")
  
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/truck")
  edit_truck_profit(args)
  flash(json.dumps({"msg": "عُدٍّل السجل"}), "info")
  return redirect("/truck")

@app.route('/truck/records/<int:id>/delete', methods=["POST"])
def truck_record_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/truck")
  if not is_truck_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/truck")
  delete_truck_profit(id)
  flash(json.dumps({"msg": "حُُذِف السجل"}), "warning")
  return redirect("/truck")

@app.route('/truck/records/delete', methods=["POST"])
def truck_record_delete_all():
  delete_truck_profit_all()
  flash(json.dumps({"msg": "حُُذِفت جميع السجلّات"}), "warning")
  return redirect("/truck")

@app.route('/mixer/records/delete', methods=["POST"])
def mixer_record_delete_all():
  delete_mixer_profit_all()
  flash(json.dumps({"msg": "حُُذِفت جميع السجلّات"}), "warning")
  return redirect("/mixer")

@app.route('/block_factory/records/delete', methods=["POST"])
def block_factory_record_delete_all():
  delete_block_factory_profit_all()
  flash(json.dumps({"msg": "حُُذِفت جميع السجلّات"}), "warning")
  return redirect("/block_factory")

# Mixer
@app.route('/mixer')
def mixer():
  return render_template('mixer.html', title='الجبّالة - السجل')

@app.route('/mixer/config', methods=["POST"])
def mixer_config():
  args = dict(request.form)
  try:
    args["purchase_price"] = int(float(args['purchase_price']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء الجبّالة قيمته غير صحيحة"}), "error")
    return redirect("/mixer")
  if not args.get('name', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون الاسم فارغا"}), "error")
    return redirect("/mixer")
  if is_mixer():
    flash(json.dumps({"msg": "خطأ: تمت اضافة الجبالة مسبقا"}), "error")
    return redirect("/mixer")

  post_mixer_config(args)
  flash(json.dumps({"msg": "أُضيفت الجبّالة"}), "success")
  return redirect("/mixer")

@app.route('/mixer/edit', methods=["POST"])
def mixer_edit():
  args = dict(request.form)
  try:
    args["purchase_price"] = int(float(args['purchase_price']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء الجبّالة قيمته غير صحيحة"}), "error")
    return redirect("/mixer")
  if not is_mixer():
    flash(json.dumps({"msg": "خطأ: لا توجد جبّالة بعد"}), "error")
    return redirect("/mixer")
  post_mixer_edit(args)
  flash(json.dumps({"msg": "عُدلت الجبّالة"}), "success")
  return redirect("/mixer")

@app.route('/mixer/records/add', methods=["POST"])
def mixer_record_add():
  args = dict(request.form)
  if not is_mixer():
    flash(json.dumps({"msg": "خطأ: لا توجد شاحنة بعد"}), "error")
    return redirect("/truck")
  try:
    args["amount"] = int(float(args['amount']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/mixer")
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/mixer")
  add_mixer_profit(args)
  flash(json.dumps({"msg": "أُضيفت الأرباح"}), "success")
  return redirect("/mixer")

@app.route('/mixer/records/<int:id>/edit', methods=["POST"])
def mixer_record_edit(id):
  args = dict(request.form)
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/mixer")
  
  if not is_mixer_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/mixer")
  args['id'] = id
  try:
    args["amount"] = int(float(args['amount']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/mixer")
  
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/mixer")
  edit_mixer_profit(args)
  flash(json.dumps({"msg": "عُدٍّل السجل"}), "info")
  return redirect("/mixer")

@app.route('/mixer/records/<int:id>/delete', methods=["POST"])
def mixer_record_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/mixer")
  if not is_mixer_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/mixer")
  delete_mixer_profit(id)
  flash(json.dumps({"msg": "حُُذِف السجل"}), "warning")
  return redirect("/mixer")

# Block factory
@app.route('/block_factory')
def block_factory():
  return render_template('block_factory.html', title='معمل البلوك - السجل')

@app.route('/block_factory/config', methods=["POST"])
def block_factory_config():
  args = dict(request.form)
  try:
    args["purchase_price"] = int(float(args['purchase_price']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء الجبّالة قيمته غير صحيحة"}), "error")
    return redirect("/block_factory")
  if not args.get('name', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون الاسم فارغا"}), "error")
    return redirect("/block_factory")
  if is_block_factory():
    flash(json.dumps({"msg": "خطأ: تمت اضافة معمل البلوك مسبقا"}), "error")
    return redirect("/block_factory")
  post_block_factory_config(args)
  flash(json.dumps({"msg": "أُضيف معمل البلوك"}), "success")
  return redirect("/block_factory")

@app.route('/block_factory/edit', methods=["POST"])
def block_factory_edit():
  args = dict(request.form)
  try:
    args["purchase_price"] = int(float(args['purchase_price']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: سعر شراء معمل البلوك قيمته غير صحيحة"}), "error")
    return redirect("/block_factory")
  if not is_block_factory():
    flash(json.dumps({"msg": "خطأ: لا يوجد معمل بلوك بعد"}), "error")
    return redirect("/block_factory")
  post_block_factory_edit(args)
  flash(json.dumps({"msg": "عُدل معمل البلوك"}), "success")
  return redirect("/block_factory")

@app.route('/block_factory/records/add', methods=["POST"])
def block_factory_record_add():
  args = dict(request.form)
  if not is_block_factory():
    flash(json.dumps({"msg": "خطأ: لا توجد شاحنة بعد"}), "error")
    return redirect("/truck")
  try:
    args["amount"] = int(float(args['amount']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/block_factory")
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/block_factory")
  add_block_factory_profit(args)
  flash(json.dumps({"msg": "أُضيفت الأرباح"}), "success")
  return redirect("/block_factory")

@app.route('/block_factory/records/<int:id>/edit', methods=["POST"])
def block_factory_record_edit(id):
  args = dict(request.form)
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/block_factory")
  
  if not is_block_factory_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/block_factory")
  args['id'] = id
  try:
    args["amount"] = int(float(args['amount']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة غير صحيحة"}), "error")
    return redirect("/block_factory")
  
  if not args.get('month_year', '').strip():
    flash(json.dumps({"msg": "خطأ: لا يمكن أن يكون التاريخ فارغا"}), "error")
    return redirect("/block_factory")
  edit_block_factory_profit(args)
  flash(json.dumps({"msg": "عُدٍّل السجل"}), "info")
  return redirect("/block_factory")

@app.route('/block_factory/records/<int:id>/delete', methods=["POST"])
def block_factory_record_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/block_factory")
  if not is_block_factory_profit_reecord(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/block_factory")
  delete_block_factory_profit(id)
  flash(json.dumps({"msg": "حُُذِف السجل"}), "warning")
  return redirect("/block_factory")

@app.route('/property')
def property():
  return render_template('property.html', title="العقارات", property=Properties().property_html_dict())

@app.route('/property/add', methods=["POST"])
def property_add():
  args = dict(request.form)
  if not (args.get('discreption', '').strip() or args.get('address', '').strip() or args.get('buy_price', '').strip() or args.get('buy_date', '').strip() or args.get('seller_name', '').strip()):
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect("/property")
  try:
    args["buy_price"] = float(args['buy_price'])
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة الشراء غير صحيحة"}), "error")
    return redirect("/property")
  add_property(args)
  flash(json.dumps({"msg": "أُضيف العقار"}), "success")
  return redirect("/property")

@app.route('/property/<int:id>/info')
def property_info(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/property")
  
  if not is_property(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/property")
  return render_template("property_info.html", title=f"عقار رقم {id}", property=Properties().get_property_with_cost_by_id(id))

@app.route('/property/<int:id>/delete', methods=["POST"])
def property_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم العقار غير صحيح"}), "error")
    return redirect(f"/property")
  if not is_property(id):
    flash(json.dumps({"msg": "خطأ: العقار غير موجود"}), "error")
    return redirect(f"/property")
  delete_property(id)
  flash(json.dumps({"msg": "حٌذِف العقار"}), "warning")
  return redirect("/property")

@app.route('/property/<int:id>/sell', methods=["POST"])
def property_sell(id):
  args = dict(request.form)
  try:
    args['id'] = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم العقار غير صحيح"}), "error")
    return redirect(f"/property")
  if not is_property(id):
    flash(json.dumps({"msg": "خطأ: العقار غير موجود"}), "error")
    return redirect(f"/property")
  sell_property(args)
  flash(json.dumps({"msg": "بِيعَ العقار"}), "success")
  return redirect("/property")

@app.route('/property/<int:id>/improvements')
def property_improvements(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect("/property")
  
  if not is_property(id):
    flash(json.dumps({"msg": "خطأ: سحل غير موجود"}), "error")
    return redirect("/property")
  return render_template("property_improvements.html", title=f"عقار رقم {id}", property=Properties().get_property_with_cost_by_id(id), property_improvements=PropertiesImprovements().get_costs_rows_by_id(id))

@app.route('/property/<int:property_id>/improvements/add', methods=["POST"])
def property_improvements_add(property_id):
  args = dict(request.form)
  try:
    args['property_id'] = int(property_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  if not (args.get('discreption', '').strip() or args.get('improve_date', '').strip()):
    flash(json.dumps({"msg": "خطأ: الرجاء ملء حميع الحقول"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  try:
    args["cost"] = float(args['cost'])
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة التكلفة غير صحيحة"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  add_property_improvements(args)
  flash(json.dumps({"msg": "أُضيف التحسين"}), "success")
  return redirect(f"/property/{property_id}/improvements")

@app.route('/property/<int:property_id>/improvements/<int:id>/delete', methods=["POST"])
def property_improvement_delete(id, property_id):
  try:
    property_id = int(property_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم العقار غير صحيح"}), "error")
    return redirect(f"/property")
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم التحسين غير صحيح"}), "error")
    return redirect(f"/property{property_id}/improvements")
  if not is_property(property_id):
    flash(json.dumps({"msg": "خطأ: العقار غير موجود"}), "error")
    return redirect(f"/property")
  if not is_improvement(id):
    flash(json.dumps({"msg": "خطأ: التحسين غير موجود"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  delete_property_improvement(id)
  flash(json.dumps({"msg": "حُُذِف التحسين"}), "warning")
  return redirect(f"/property/{property_id}/improvements")

@app.route('/property/<int:property_id>/improvements/delete', methods=["POST"])
def property_improvements_delete(property_id):
  try:
    property_id = int(property_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم العقار غير صحيح"}), "error")
    return redirect(f"/property")
  if not is_property(property_id):
    flash(json.dumps({"msg": "خطأ: العقار غير موجود"}), "error")
    return redirect(f"/property")
  if not is_property_has_improvement(property_id):
    flash(json.dumps({"msg": "خطأ: العقار لا يحتوي على تحسينات"}), "error")
    return redirect(f"/property")
  delete_property_improvements(property_id)
  flash(json.dumps({"msg": "حُُذِفت التحسينات"}), "warning")
  return redirect(f"/property/{property_id}/improvements")

@app.route('/property/<int:property_id>/edit', methods=["POST"])
def property_edit(property_id):
  args = dict(request.form)
  try:
    args['id'] = int(property_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم العقار غير صحيح"}), "error")
    return redirect(f"/property")
  try:
    args["buy_price"] = int(float(args['buy_price']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة الشراء غير صحيحة"}), "error")
    return redirect("/property")
  if not is_property(property_id):
    flash(json.dumps({"msg": "خطأ: العقار غير موجود"}), "error")
    return redirect(f"/property")
  if not (args.get('discreption', '').strip() or args.get('address', '').strip() or args.get('buy_price', '').strip() or args.get('buy_date', '').strip() or args.get('seller_name', '').strip()):
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect("/property")
  edit_property(args)
  flash(json.dumps({"msg": "عُدٍّل العقار"}), "success")
  return redirect(f"/property/{property_id}/info")
  
@app.route('/property/<int:property_id>/improvements/<int:id>/edit', methods=["POST"])
def property_improvements_edit(property_id, id):
  args = dict(request.form)
  try:
    args['property_id'] = int(property_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم عقار غير صحيح"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  try:
    args['id'] = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم التحسين غير صحيح"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  if not (args.get('description', '').strip() or args.get('improve_date', '').strip()):
    flash(json.dumps({"msg": "خطأ: الرجاء ملء حميع الحقول"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  try:
    args["cost"] = int(float(args['cost']))
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: قيمة التكلفة غير صحيحة"}), "error")
    return redirect(f"/property/{property_id}/improvements")
  edit_property_improvements(args)
  flash(json.dumps({"msg": "عًدٍّل التحسين"}), "success")
  return redirect(f"/property/{property_id}/improvements")

# Customer
@app.route('/customer')
def customer():  
  return render_template('customer.html', title='الزبائن - الأرصدة',  customer=Customers().customer_html_dict())

@app.route('/customer/add', methods=["POST"])
def customer_add():
  args = dict(request.form)
  if not args.get('name', '').strip():
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect("/customer")
  add_customer(args)
  flash(json.dumps({"msg": "أُضيف الزبون"}), "success")
  return redirect("/customer")

@app.route('/customer/<int:id>/edit', methods=["POST"])
def customer_edit(id):
  args = dict(request.form)
  if not args.get('name', '').strip():
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect("/customer")
  try:
    args['id'] = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم زبون غير صحيح"}), "error")
    return redirect(f"/customer")
  edit_customer(args)
  flash(json.dumps({"msg": "عُِدٍّل الزبون"}), "success")
  return redirect(f"/customer/{id}/records")

@app.route('/customer/<int:id>/delete', methods=["POST"])
def customer_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم زبون غير صحيح"}), "error")
    return redirect(f"/customer")
  delete_customer(id)
  flash(json.dumps({"msg": "حُذِفَ الزبون"}), "success")
  return redirect(f"/customer")

@app.route('/customer/delete', methods=["POST"])
def customers_delete():
  delete_customers()
  flash(json.dumps({"msg": "حُذِفَ الزبائن"}), "success")
  return redirect(f"/customer")

@app.route('/customer/<int:id>/records')
def customer_records(id):  
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم عقار غير صحيح"}), "error")
    return redirect(f"/customer")
  print(Customers().get_customer_by_id_with_balance(id))
  print(CustomerRecord().get_customer_records_by_id(id))
  return render_template('customer_record.html', title='الزبائن - الأرصدة',  customer=Customers().get_customer_by_id_with_balance(id), records = CustomerRecord().get_customer_records_by_id(id))

@app.route('/customer/<int:id>/records/add', methods=["POST"])
def customer_record_add(id):
  args = dict(request.form)
  if not args.get('amount', '').strip():
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect(f"/customer/{id}/records")
  args['customer_id'] = id
  add_customer_record(args)
  flash(json.dumps({"msg": "أُضيف السجل"}), "success")
  return redirect(f"/customer/{id}/records")

@app.route('/customer/<int:id>/records/<int:record_id>/edit', methods=["POST"])
def customer_record_edit(id, record_id):
  args = dict(request.form)
  if not args.get('amount', '').strip():
    flash(json.dumps({"msg": "خطأ: الرجاء ملئ جميع الحقول الإجبارية"}), "error")
    return redirect(f"/customer/{id}/records")
  try:
    args['customer_id'] = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم زبون غير صحيح"}), "error")
    return redirect(f"/customer")
  try:
    args['id'] = int(record_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect(f"/customer{id}/records")
  edit_customer_record(args)
  flash(json.dumps({"msg": "عُِدٍّل السجل"}), "success")
  return redirect(f"/customer/{id}/records")

@app.route('/customer/<int:id>/records/<int:record_id>/delete', methods=["POST"])
def customer_record_delete(id, record_id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم زبون غير صحيح"}), "error")
    return redirect(f"/customer")
  try:
    record_id = int(record_id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم سحل غير صحيح"}), "error")
    return redirect(f"/customer{id}/records")
  delete_customer_record(record_id)
  flash(json.dumps({"msg": "حُذِفَ السجل"}), "success")
  return redirect(f"/customer/{id}/records")

@app.route('/customer/<int:id>/records/delete', methods=["POST"])
def customer_records_delete(id):
  try:
    id = int(id)
  except (ValueError, TypeError, KeyError):
    flash(json.dumps({"msg": "خطأ: رقم زبون غير صحيح"}), "error")
    return redirect(f"/customer")
  delete_customer_records(id)
  flash(json.dumps({"msg": "حُذِفَت السجلّات"}), "success")
  return redirect(f"/customer")

@app.route('/crop')
def crop():
  return render_template("crop.html", title="المحاصيل", crop=Crop().crop_html_dict(data=False), property=Properties().property_html_dict())



























































if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5005,debug=True)