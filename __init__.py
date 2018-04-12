from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    return 'login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    return 'register'


if __name__ == '__main__':
    app.run(debug=True)