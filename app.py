from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL Connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bd_app'
mysql.init_app(app)

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def menu_principal():
    return render_template("menu_principal.html")


# ##################################### E Q U I P O S / M A N T E N I M I E N T O ################################################
@app.route('/equipos')
def Index_equipos():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM equipos')
    data = cursor.fetchall()
    return render_template('index_equipos.html', equipments=data)

# Agregar equipos
@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        fecha_mantto_prog = request.form['fecha_mantto_prog']
        fecha_mantto_real = request.form['fecha_mantto_real']
        # cursor = mysql.get_db().cursor()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO equipos (name, location, fecha_mantto_prog, fecha_mantto_real) VALUES (%s, %s, %s, %s)',
                       (name, location, fecha_mantto_prog, fecha_mantto_real))
        # mysql.connection.commit()
        conn.commit()
        conn.close()
        flash('Equipment Added Successfully')
        return redirect(url_for('Index_equipos'))

# Obtener equipo para editar
@app.route('/edit_equipos/<id>')
def get_equipment(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM equipos WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('edit_equipment.html', equipment=data[0])


# Update equipo
@app.route('/update_equipos/<id>', methods=['POST'])
def update_equipment(id):
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        fecha_mantto_prog = request.form['fecha_mantto_prog']
        fecha_mantto_real = request.form['fecha_mantto_real']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE equipos
            SET name = %s,
                location = %s,
                fecha_mantto_prog = %s,
                fecha_mantto_real = %s
            WHERE id = %s
        """, (name, location, fecha_mantto_prog, fecha_mantto_real, id))
        conn.commit()
        conn.close()
        flash('Contact Update Successfully')
        return redirect(url_for('Index_equipos'))

# Borrar equipos
@app.route('/delete_equipos/<string:id>')
def delete_equipment(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipos WHERE id = {0}'.format(id))
    conn.commit()
    conn.close()
    flash('Equipment Removed Successfully')
    return redirect(url_for('Index_equipos'))

# ##################################### E N E R G E T I C O S ################################################
@app.route('/energy')
def Index_energy():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM monthly_consumption_energy')
    data = cursor.fetchall()
    return render_template('index_energy.html', consumptions=data)

# Agregar equipos
@app.route('/add_consumption', methods=['POST'])
def add_consumption():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        water_consumption = request.form['water_consumption']
        electricity_consumption = request.form['electricity_consumption']
        gasoline_consumption = request.form['gasoline_consumption']
        gas_consumption = request.form['gas_consumption']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO monthly_consumption_energy (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption) VALUES (%s, %s, %s, %s, %s, %s)',
                       (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption))
        conn.commit()
        conn.close()
        flash('Consumption Added Successfully')
        return redirect(url_for('Index_energy'))

# Obtener equipo para editar
@app.route('/edit_energy/<id>')
def get_consumption(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM monthly_consumption_energy WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('edit_consumption.html', consumption=data[0])


# Update equipo
@app.route('/update_energy/<id>', methods=['POST'])
def update_consumption(id):
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        water_consumption = request.form['water_consumption']
        electricity_consumption = request.form['electricity_consumption']
        gasoline_consumption = request.form['gasoline_consumption']
        gas_consumption = request.form['gas_consumption']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE monthly_consumption_energy
            SET year = %s,
                month = %s,
                water_consumption = %s,
                electricity_consumption = %s,
                gasoline_consumption = %s,
                gas_consumption = %s
            WHERE id = %s
        """, (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption, id))
        conn.commit()
        conn.close()
        flash('Consumption Update Successfully')
        return redirect(url_for('Index_energy'))

# Borrar equipos
@app.route('/delete_energy/<string:id>')
def delete_consumption(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM monthly_consumption_energy WHERE id = {0}'.format(id))
    conn.commit()
    conn.close()
    flash('Consumption Removed Successfully')
    return redirect(url_for('Index_energy'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
