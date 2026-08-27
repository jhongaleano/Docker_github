from flask import Flask,request,render_template,redirect,url_for
import pymysql
import time
import os
app = Flask("__name__")


BD = {

    'host':"servidor-bd-ejemplo",
    'user':"root",
    'password':os.getenv("MYSQL_ROOT_PASSWORD"),
    'database':"adso_bd",
    'connect_timeout':3,
    'cursorclass':pymysql.cursors.DictCursor,
}

def get_connect():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            return pymysql.connect(**BD)
        except pymysql.err.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Base de datos no lista aún. Esperando... (Intento {attempt + 1}/{max_retries})")
                time.sleep(3)
            else:
                raise e

def table_BD():
    connection = get_connect()

    try:
        with connection.cursor() as cursor:
            sql_create_table = """ 
            CREATE TABLE IF NOT EXISTS aprendices (
             id INT AUTO_INCREMENT PRIMARY KEY,
             nombre_completo VARCHAR(100) NOT NULL,
             numero_documento VARCHAR(20) NOT NULL,
             ficha VARCHAR(20) NOT NULL,
             creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
             """
            cursor.execute(sql_create_table)
            connection.commit()

    finally:
        connection.close()








@app.route("/")
def main():
    bd_status = ""
    aprendices = []

    try:
        conn = get_connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM aprendices ORDER BY id DESC")
            aprendices = cursor.fetchall()
        conn.close()
        bd_status = "CONEXION EXITOSA Y PRUEBA DE CI/CD y TEST EXITOSO"
    except Exception as e:
        bd_status = f"Error de conexión: {e}"

    return render_template("index.html", bd_status = bd_status, aprendices = aprendices)
      

@app.route("/registro", methods=['POST'])

def registro():
    connection = get_connect()

    try:
        if request.method == 'POST':
            nombre_completo = request.form.get('nombre_completo')
            numero_documento = request.form.get('numero_documento')
            ficha = request.form.get('ficha')


            #print(f"DATOS RECIBIDOS -> Nombre: {nombre_completo}, Doc: {numero_documento}, Ficha: {ficha}")

            sql ='INSERT INTO aprendices (nombre_completo,numero_documento,ficha) VALUES (%s,%s,%s)'
            with connection.cursor() as cursor:
                 cursor.execute(sql,(nombre_completo,numero_documento,ficha))
            connection.commit()
    finally:
        connection.close()

    # 3. Redireccionar al usuario a la vista principal
    return redirect(url_for('main'))


if __name__ == '__main__':
    hostPort = os.getenv("HOST","0.0.0.0") # nosec B104
    #debug = os.getenv("DEBUG","False").lower()in ("true","1")
    table_BD()
    app.run(host=hostPort, port=5050, debug=True)