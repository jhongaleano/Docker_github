from flask import Flask,request,render_template,redirect,url_for
import pymysql

app = Flask("__name__")


BD = {

    'host':"servidor-bd",
    'user':"root",
    'password':"sena123",
    'database':"adso_bd",
    'connect_timeout':3,
    'cursorclass':pymysql.cursors.DictCursor
}

def get_connect():
    return pymysql.connect(**BD)

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



table_BD()




@app.route("/",methods=['GET'])
def main():
    connection = get_connect()

    try:

        if request.method == 'GET':
            sql_select = "SELECT id, nombre_completo, numero_documento, ficha, creado_en FROM aprendices"

            with connection.cursor() as cursor:
                cursor.execute(sql_select)
                aprendices = cursor.fetchall()

            return render_template('index.html',aprendices = aprendices)
    finally:
        connection.close()
      

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
    app.run(host="0.0.0.0", port=5050, debug=True)