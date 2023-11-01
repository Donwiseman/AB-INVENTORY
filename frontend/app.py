from flask import Flask, render_template, request, redirect, url_for, session
from os import getenv
from models import storage, User, Inventory

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
            # Wrong Username
            return redirect(url_for('signin'))
        user = user_list[0]
        if user.verify_password(password):
            session['username'] = username
            return f"You're logged in {user.first_name}"
        else:
            return redirect(url_for('signin'))
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'], strict_slashes=False)
def signup():
    """ Sign Up page. """
    if request.method == 'POST':
        if request.form['pword'] != request.form['rpword']:
            return redirect(url_for('signup'))
        if storage.get_users(request.form['username']):
            return redirect(url_for('signup'))
        if len(request.form['pword']) < 7:
            return redirect(url_for('signup'))
        new_user = User(request.form['lname'], request.form['fname'],
                        request.form['username'], request.form['email'],
                        request.form['pword'], request.form['rq'],
                        request.form['ra'])
        storage.add(new_user)
        storage.save()
        session['username'] = new_user.username
        return f"You're logged in {new_user.first_name}"
    return render_template('signup.html')


@app.route('/signout', strict_slashes=False)
def signout():
    """ Signs user out of session. """
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
