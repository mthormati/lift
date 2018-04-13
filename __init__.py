from flask import Flask, render_template, url_for, request, session, redirect
from variables import *
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

@app.route('/')
def index():
    errorMessage = ''
    return render_template('index.html', errorMessage=errorMessage)

@app.route('/login', methods=['POST'])
def login():
    return 'login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)