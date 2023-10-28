from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    return render_template('home.html')


@app.route('/login.html', strict_slashes=False)
def login():
    return render_template('login.html')


@app.route('/signup.html', strict_slashes=False)
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
