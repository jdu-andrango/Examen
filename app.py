from flask import Flask, send_file,jsonify, request
from psycopg2 import connect,extras

app= Flask(__name__)

host='localhost'
port=5432
database='flaskJonathan'
user='postgres'
password='david'

def getConexion():
    conexion= connect(host=host,port=port,database=database,user=user,password=password)
    return conexion


@app.get('/')
def index():
    return send_file('static/index.html')

@app.get('/jonathan/docente')
def docente():
    conexion=getConexion()
    curSor=conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM docente')
    docente= curSor.fetchall()
    curSor.close()
    conexion.close()
    return jsonify(docente)

@app.post('/jonathan/docente')
def enviarDocente():
    
    nuevoDocente= request.get_json()
    
    nombre = nuevoDocente['nombre']
    apellido = nuevoDocente['apellido']
    catedra=nuevoDocente['catedra']
    facultad=nuevoDocente['facultad']
    paralelo=nuevoDocente['paralelo']
    jornada=nuevoDocente['jornada']
    
    conexion=getConexion()
    curSor=conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('INSERT INTO docente (nombre, apellido, catedra, facultad, paralelo, jornada) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *',(nombre, apellido, catedra, facultad, paralelo, jornada))
    newDocente= curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    
    
    return jsonify(newDocente)



@app.get('/jonathan/docente/<id>')
def traerDocentes(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM docente WHERE id = %s ', (id, ))
    traerDocente=curSor.fetchone()
    
    
    if traerDocente is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerDocente)
    return jsonify(traerDocente)
    

@app.delete('/jonathan/docente/<id>')
def deleteDocente(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM docente WHERE id = %s RETURNING *', (id, ))
    docenteEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if docenteEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(docenteEliminado)


@app.put('/jonathan/docente/<id>')
def updateDocente(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newDocente= request.get_json()
   
    nombre = newDocente['nombre']
    apellido= newDocente['apellido']
    catedra= newDocente['catedra']
    facultad=newDocente ['facultad']
    paralelo= newDocente['paralelo']
    jornada=newDocente ['jornada']
    
    curSor.execute('UPDATE docente SET nombre= %s, apellido= %s, catedra= %s, facultad= %s,paralelo= %s,jornada= %s WHERE id=%s RETURNING *',(nombre, apellido, catedra, facultad, paralelo, jornada,id))
    docenteActualizado=curSor.fetchone()
    
    conexion.commit()
    curSor.close()
    conexion.close()
    
    if docenteActualizado is None:
        return jsonify({'message':'automovil no encontrado'}),404
    

    return jsonify(docenteActualizado)


if __name__=='__main__':
    app.run(debug=True)