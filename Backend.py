from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS  # Permite que el frontend acceda a la API

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir solicitudes desde el navegador

port = 3000

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Admin123!",
    "database": "Dispositivos"
}

# Ruta para obtener dispositivos con sus ubicaciones y mediciones
@app.route('/api/dispositivos', methods=['GET'])
def get_dispositivos():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT d.id_dispositivo, d.nombre, d.descripcion, 
                   u.latitud, u.longitud, 
                   GROUP_CONCAT(CONCAT(m.tipo_medicion, ': ', m.valor, ' ', m.unidad) SEPARATOR ', ') AS mediciones
            FROM Dispositivos d
            LEFT JOIN Ubicaciones u ON d.id_dispositivo = u.id_dispositivo
            LEFT JOIN Mediciones m ON d.id_dispositivo = m.id_dispositivo
            GROUP BY d.id_dispositivo, u.latitud, u.longitud;
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=port, host="0.0.0.0")  # Permite que otros dispositivos accedan a la API
