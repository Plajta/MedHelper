from flask import Flask, render_template, redirect, request

app = Flask("PlajtaMed", template_folder='src/frontend/templates', static_url_path='/static', static_folder='src/frontend/static')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', user="Damongus Veliký", position="Bůh všehomíra", auth="69")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == "amogus" and pwd == "ballz":
            return redirect("admin")
        return "Blbečku!"
    else:
        return render_template('login.html')
