from flask import Flask, render_template, redirect, request

app = Flask("PlajtaMed", template_folder='src/frontend/templates', static_url_path='/static', static_folder='src/frontend/static')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form['fname']
        lastname = request.form['lname']
        birth = request.form['birth']

        print(name)


    return render_template('admin.html')

@app.route("/about")
def about():
    return render_template("about.html")

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
