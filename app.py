from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app= Flask(__name__)
app.config

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '5248'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/dashboard.html')
def dashboard():
    if 'correo' in session:
        correo = session['correo']
        cur = mysql.connection.cursor()
        cur.execute('SELECT nombre FROM pacientes WHERE correo=%s', (correo,))
        record = cur.fetchone()
        if record:
            nombre = record[0]
            return render_template('dashboard.html', correo=correo, nombre=nombre)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'correo' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/pacientes.html')
def patients():
    return render_template("pacientes.html")

@app.route('/citas.html')
def citas():
    return render_template("citas.html")

@app.route('/contactos.html')
def contactos():
    return render_template("contactos.html")

@app.route('/inicio.html', methods=['GET','POST'])
def inicio():
    return render_template("inicio.html")

@app.route('/logout.html', methods=['GET','POST'])
def logout():
    session.pop('correo', None)
    return redirect(url_for('index'))

@app.route('/add.html', methods=['POST'])
def add():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido_pat = request.form["apellido_pat"]
        apellido_mat = request.form["apellido_mat"]
        correo = request.form["correo"]
        password = request.form["password"]
        telefono = request.form["telefono"]
        cuidad = request.form["cuidad"]
        sexo = request.form["sexo"]
        cur = mysql.connection.cursor()
        
        # Para ver si ya esta registrado el correo
        cur.execute("SELECT correo FROM pacientes WHERE correo=%s", (correo,))
        result = cur.fetchone()
        if result:
            flash("Este correo ya esta registrado.")
            return redirect(url_for("registro"))

        # agrega el nuevo usuario
        cur.execute("INSERT INTO pacientes (nombre, apellido_pat, apellido_mat, correo, password, telefono, cuidad, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (nombre, apellido_pat, apellido_mat, correo, password, telefono, cuidad, sexo))
        mysql.connection.commit()
        flash("La cuenta se creo con exito!")
        return redirect(url_for("inicio"))

@app.route('/login.html', methods=['GET','POST'])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")
        if correo and password:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM pacientes WHERE correo=%s AND password=%s', (correo,password))
            record = cur.fetchone()
            if record:
                session['loggedin'] = True
                session['correo'] = correo
                session['nombre'] = record[0] 
                return redirect(url_for("dashboard"))
            else:
                flash("Correo o Password Invalidos!")
        else:
            flash("Correo o Password Invalidos!")
    return redirect(url_for("inicio"))

@app.route('/registro.html')
def registro():
    return render_template("registro.html")


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port= 8000)
