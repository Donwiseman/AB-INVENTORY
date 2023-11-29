from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from os import getenv
from models import storage, User, Inventory
import pytz

app = Flask(__name__)
app.secret_key = getenv('AB_SECRET')


@app.route('/', strict_slashes=False)
def home():
    """ Homepage of website. """
    return render_template('home.html')


@app.route('/signin', methods=['POST', 'GET'], strict_slashes=False)
def signin():
    """ Sign In page. """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_list = storage.get_users(username)
        if not user_list:
            # Check if email is used instead of username
            user_list = storage.user_via_email(username)
            if not user_list:
                session['error'] = 'username'
                return redirect(url_for('signin'))
        user = user_list[0]
        if user.verify_password(password):
            session['username'] = user.username
            session.pop('error', None)
            return redirect(url_for('dashboard'))
        else:
            session['error'] = 'password'
            return redirect(url_for('signin'))
    return render_template('login.html', error=session.get('error'))


@app.route('/signup', methods=['POST', 'GET'], strict_slashes=False)
def signup():
    """ Sign Up page. """
    if request.method == 'POST':
        if storage.get_users(request.form['username']):
            session['error'] = 'username'
            return redirect(url_for('signup'))
        if storage.user_via_email(request.form['email']):
            session['error'] = 'email'
            return redirect(url_for('signup'))
        new_user = User(request.form['lname'], request.form['fname'],
                        request.form['username'], request.form['email'],
                        request.form['pword'], request.form['rq'],
                        request.form['ra'])
        storage.add(new_user)
        storage.save()
        session['username'] = new_user.username
        session.pop('error', None)
        return redirect(url_for('dashboard'))
    return render_template('signup.html', error=session.get('error'))


@app.route('/signout', strict_slashes=False)
def signout():
    """ Signs user out of session. """
    session.pop('username', None)
    session.pop('inventory_id', None)
    return redirect(url_for('home'))


@app.route('/dashboard', methods=['POST', 'GET'], strict_slashes=False)
def dashboard():
    """ Displays user specific dashboard. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', user=user,
                           timezones=pytz.common_timezones)


@app.route('/inventory/<inventory_id>', strict_slashes=False)
def inventory(inventory_id):
    """ Displays user choosen inventory Page. """
    try:
        user = storage.get_users(session['username'])[0]
        inv = storage.get_inventory(inventory_id)[0]
        session['inventory_id'] = inventory_id
    except Exception:
        return redirect(url_for('dashboard'))
    return render_template('inventory.html', user=user,
                           timezones=pytz.common_timezones, inv=inv)


@app.route('/inventory/create', methods=['POST'], strict_slashes=False)
def add_inventory():
    """ Creates an inventory for the user. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        inv = user.create_inventory(request.form['inventory-name'],
                                    request.form['timezone'])
        if inv:
            return redirect(url_for('inventory', inventory_id=inv.id))
    return redirect(url_for('dashboard'))


@app.route('/inventory/items', strict_slashes=False)
def items():
    """ Shows a list of all items in a given inventory. """
    try:
        user = storage.get_users(session['username'])[0]
        inv = storage.get_inventory(session['inventory_id'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return render_template('items.html', user=user,
                           timezones=pytz.common_timezones, inv=inv)


@app.route('/inventory/transactions', strict_slashes=False)
def show_transactions():
    """ Shows all transactions by a user_inventory. """
    try:
        inv = storage.get_inventory(session['inventory_id'])[0]
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return f"Still working...."


@app.route('/inventory/search/<query>', strict_slashes=False)
def search_item(query):
    """ returns items based on the search parameter """
    try:
        inv = storage.get_inventory(session['inventory_id'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    result = []
    search_items = inv.search_item(query)
    if search_items:
        for item in search_items:
            item_detail = [ item.name, item.id, item.quantity, item.cost_price,
                           item_sale_price, item.category, item.alert_level]
            result.append(item_detail)
    return jsonify(results)


@app.route('/inventory/items/remove', strict_slashes=False)
def remove_item():
    """ removes or deletes an item from the inventory. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return f"deleting an item...."


@app.route('/inventory/item/create', methods=['POST'], strict_slashes=False)
def create_item():
    """ Creates a new item in the choosen inventory."""
    try:
        inv = storage.get_inventory(session['inventory_id'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        try:
            item = inv.create_item(request.form['name'],
                                   request.form['cost_price'],
                                   request.form['sale_price'],
                                   request.form['quantity'],
                                   request.form['total'],
                                   request.form['unit'],
                                   request.form['category'],
                                   request.form['alert_level'])
            return "item.name has been created"
        except Exception:
            return "Failed"
    else:
        return "Failed"


@app.route('/inventory/item/add', methods=['POST'], strict_slashes=False)
def add_item():
    """ adds more quantities of an item."""
    try:
        inv = storage.get_inventory(session['inventory_id'])[0]
        item = storage.get_item(request.form['item_id'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    trans = inv.add_item(item, request.form['purchase_cost'],
                         request.form['details'])
    return jsonify(trans.print_transaction())


@app.route('/inventory/sale/', strict_slashes=False)
def sale():
    """ make a sale order"""
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return f"Making sale order"


@app.route('/inventory/alerts', strict_slashes=False)
def alerts():
    """ Page dealing with alert settings for low items. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return f"Showing your alert settings...."


@app.teardown_appcontext
def app_teardown(exception=None):
    """ Help in closing each request session. """
    storage.end_session()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
