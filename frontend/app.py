from flask import Flask, render_template, request, redirect, url_for, session
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
            session['username'] = username
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
    return redirect(url_for('home'))


@app.route('/dashboard', methods=['POST', 'GET'], strict_slashes=False)
def dashboard():
    """ Displays user specific dashboard. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', user=user)


@app.route('/inventory/<inventory_id>', strict_slashes=False)
def inventory(inventory_id):
    """ Displays user choosen inventory Page. """
    try:
        inv = storage.get_inventory(inventory_id)[0]
        session['inventory_id'] = inventory_id
    except Exception:
        return redirect(url_for('dashboard'))
    return f"You are viewing your {inv.name}"


@app.route('/inventory/create', methods=['POST', 'GET'], strict_slashes=False)
def add_inventory():
    """ Creates an inventory for the user. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return render_template('create_inv.html', user=user)


@app.route('/inventory/transactions', strict_slashes=False)
def show_transactions():
    """ Shows all transactions by a user_inventory. """
    try:
        user = storage.get_users(session['username'])[0]
    except Exception:
        return redirect(url_for('dashboard'))
    return f"Still working...."


@app.teardown_appcontext
def app_teardown(exception=None):
    """ Help in closing each request session. """
    storage.end_session()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
