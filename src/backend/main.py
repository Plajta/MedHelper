from flask import Flask, render_template

app = Flask("PlajtaMed", template_folder='src/frontend/templates', static_url_path='/static', static_folder='src/frontend/static')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login')
def login():
    return render_template('login.html')

