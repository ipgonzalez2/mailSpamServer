import os
import re
from flask import Flask, render_template, request, redirect, url_for
from forms import FilterForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader
#from models import Filter
app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres_user:postgres_pass@localhost:5432/filters_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    filters = []
    return render_template("index.html", filters = filters)


@app.route("/filter/", methods=["GET", "POST"])
def filter_form():
    form = FilterForm()
    if form.validate_on_submit():
        porcentaje = form.porcentaje.data
        image_name = None
        if 'spamFile' in request.files:
            file = request.files['spamFile']
            if file.filename:
                image_name = secure_filename(file.filename)
                images_dir = './spams'
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)

        fileSpam = open(file_path, 'r')
        regex = re.compile('\n\n')
        match = re.search(regex, fileSpam.read())
        inicioMensaje = match.end()
        tamanhoTotal = os.stat(file_path).st_size
        tamanhoMensaje = tamanhoTotal - inicioMensaje

        numCar = int(float(tamanhoMensaje*float((float(porcentaje)/100))))
        car = []
        x = int(float(tamanhoMensaje/numCar))
        fileSpam = open(file_path, 'r')

        for i in range(numCar):
            desp = inicioMensaje + (x * i)
            car.append(fileSpam.read()[desp])
            fileSpam.seek(0,0)


        fileSpam.close()
        print(car)


        file_loader = FileSystemLoader('spams')
        env = Environment(loader=file_loader)
        template = env.get_template('filter.c')
        output = template.render(tam = tamanhoMensaje, numCar = numCar, caracteres = car)
        with open("./spams/filter1.c", "w") as fh:
            fh.write(output)

        return redirect(url_for('index'))
    return render_template("filter_form.html", form=form)