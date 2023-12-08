import os
from flask import Flask, render_template

template_dir = os.path.abspath('../frontend/')
app = Flask("PlajtaMed", template_folder=template_dir)

@app.route('/')
def index():
    return render_template('admin.html')
