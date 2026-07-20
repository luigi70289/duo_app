import os
import csv
import sqlite3
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB_FILE = 'torneo.db'

# 🎖️ CATÁLOGO GLOBAL DE MEDALLAS
MEDALLAS_TOTALES = {
    "oro_xp": "Titán de XP (Máximo XP de la semana)",
    "hierro_tiempo": "Cerebro de Oro (Más tiempo de estudio)",
    "racha_legendaria": "Racha Legendaria (7 o más días activos)",
    "francotirador": "Francotirador (90% o más de precisión)",
    "corrector_errores": "Corrector de Errores (Repasó fallos en clase)"
}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jugadores (
            usuario TEXT PRIMARY KEY,
            xp INTEGER,
            racha INTEGER,
            tiempo INTEGER,
            precision TEXT,
            medallas TEXT,
            num_medallas INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def procesar_logros(xp, racha, precision, errores, es_max_xp, es_max_tiempo, tiempo):
    medallas = []
    if es_max_xp and int(xp) > 0:
        medallas.append("oro_xp")
    if es_max_tiempo and int(tiempo) > 0:
        medallas.append("hierro_tiempo")
    if int(racha) >= 7:
        medallas.append("racha_legendaria")
    if float(precision) >= 90.0:
        medallas.append("francotirador")
    if int(errores) > 0:
        medallas.append("corrector_errores")
    return medallas

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jugadores ORDER BY num_medallas DESC, xp DESC')
    filas = cursor.fetchall()
    conn.close()
    
    ranking = []
    for fila in filas:
        datos_jugador = dict(fila)
        datos_jugador['listado_medallas'] = json.loads(datos_jugador['medallas']) if datos_jugador['medallas'] else []
        ranking.append(datos_jugador)
        
    return render_template('index.html', ranking=ranking, catalogo=MEDALLAS_TOTALES)

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return redirect('/')

    stream = file.stream.read().decode("utf-8").splitlines()
    lector = list(csv.DictReader(stream))
    
    max_xp = -1
    max_tiempo = -1
    user_max_xp = ""
    user_max_tiempo = ""
    
    for fila in lector:
        usuario = fila.get('Username') or fila.get('Usuario') or "Desconocido"
        xp = int(fila.get('Total XP') or fila.get('XP Total') or 0)
        tiempo = int(fila.get('Time Spent (min)') or fila.get('Tiempo de estudio') or 0)
        
        if xp > max_xp:
            max_xp = xp
            user_max_xp = usuario
        if tiempo > max_tiempo:
            max_tiempo = tiempo
            user_max_tiempo = usuario

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for fila in lector:
        usuario = fila.get('Username') or fila.get('Usuario') or "Desconocido"
        xp = int(fila.get('Total XP') or fila.get('XP Total') or 0)
        racha = int(fila.get('Streak') or fila.get('Racha') or 0)
        precision = fila.get('Accuracy') or fila.get('Precisión') or "90.0" 
        tiempo = int(fila.get('Time Spent (min)') or fila.get('Tiempo de estudio') or 0)
        errores = int(fila.get('Mistakes Reviewed') or fila.get('Errores revisados') or 0)

        precision_limpia = precision.replace('%', '').strip()
        
        es_max_xp = (usuario == user_max_xp)
        es_max_tiempo = (usuario == user_max_tiempo)
        
        listado_med = procesar_logros(xp, racha, precision_limpia, errores, es_max_xp, es_max_tiempo, tiempo)
        medallas_json = json.dumps(listado_med)
        num_med = len(listado_med)

        cursor.execute('''
            INSERT INTO jugadores (usuario, xp, racha, tiempo, precision, medallas, num_medallas)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(usuario) DO UPDATE SET
                xp=excluded.xp,
                racha=excluded.racha,
                tiempo=excluded.tiempo,
                precision=excluded.precision,
                medallas=excluded.medallas,
                num_medallas=excluded.num_medallas
        ''', (usuario, xp, racha, tiempo, f"{precision_limpia}%", medallas_json, num_med))

    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
