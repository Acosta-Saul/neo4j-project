from neo4j import GraphDatabase
from flask import Flask ,render_template, url_for, request


# conexion a BD ce
user = "neo4j"
password = "AKXvKuq9x2ujefjpD2QVhkl7iJynyqpQEu3DTRVgs-8"
uri = "neo4j+s://f9bb7262.databases.neo4j.io"

driver = GraphDatabase.driver(uri=uri, auth=(user, password))
session = driver.session()

# creacion de la app con Flask
app = Flask(__name__)


#ejecuta consultas de Neo4j
def ejecutar_consulta(cypher_query):
    with driver.session() as session:
        result = session.run(cypher_query)
        return result.data()

def obtener_nodos_relacionados(nombre_nodo_raiz):
    cypher_query = f"MATCH (n:User {{name: '{nombre_nodo_raiz}'}})-[]-(x) RETURN x"
    resultados = ejecutar_consulta(cypher_query)
    return [registro['x'] for registro in resultados]






# ruta inicial
@app.route('/')
def index():
  #crear rutas
  print(url_for('index'))
  print(url_for('interfaz1'))
  print(url_for('interfaz2'))
  print(url_for('interfaz3'))
  print(url_for('interfaz4'))
  return render_template('index.html')




# Página que hace la consultas
@app.route('/read')
def interfaz1():
  return render_template('interfaz1.html')



# Página para crear nuevos nodos
@app.route('/create', methods=['GET','POST'])
def interfaz2():
  
  bandera = '0'
# Fase 1 escoger el árbol
  if request.method == 'POST' and request.form['bandera'] == '1':
    arbol_seleccionado = request.form['arbol']
    bandera = request.form['bandera']
    
    nodos_relacionados = obtener_nodos_relacionados(arbol_seleccionado)

    return render_template('interfaz2.html', nodos=nodos_relacionados, bandera = bandera)

# Fase 2 escoger el nodo al cual va estar relacionado y su tipo de relación
  if request.method == 'POST' and request.form['bandera'] == '2':
    nodo = request.form['nodo']
    relacion = request.form['relacion']
    bandera = request.form['bandera']
   
    return render_template('interfaz2.html', bandera = bandera, nodo = nodo,relacion = relacion)
  
# Fase 3 preparar los datos del nuevo nodo e insertar
  if request.method == 'POST' and request.form['bandera'] == '3':

    new_node = {
      'nombre': request.form['nombre'],
      'apellido': request.form['apellido'],
      'edad': request.form['edad'],
      'actividad':request.form['actividad'],
      'gustos': [request.form['gusto1'],request.form['gusto2']],
      'disgusto': request.form['disgusto'],
      'defuncion': request.form['defuncion'],
      'nodo_asignado': request.form['nodo_dirigido'], 
      'relacion':request.form['relacion_dirigida'],
    }
    bandera = request.form['bandera']

# query para crea el nodo
    query = """
      CREATE (:User {
        name: $name,
        apellido: $apellido,
        edad: $edad,
        actividad: $actividad,
        gustos: $gustos,
        disgusto: $disgusto,
        defuncion: $defuncion
      })
      """
#ejecuta la query
    result = session.run(query, name=new_node['nombre'], apellido=new_node['apellido'], edad=new_node['edad'], actividad=new_node['actividad'], gustos=new_node['gustos'], disgusto=new_node['disgusto'], defuncion=new_node['defuncion'])

# Obtiene el id del nodo creado para relacionar
    query_obtener_id = """
    MATCH (n:User {name: $nombre, apellido: $apellido, edad: $edad, actividad:     $actividad, gustos: $gustos, disgusto: $disgusto, defuncion: $defuncion})
    RETURN id(n) AS id_nodo
    """
#ejecuta la query  
    result_id = session.run(query_obtener_id, nombre=new_node['nombre'], apellido=new_node['apellido'], edad=new_node['edad'], actividad=new_node['actividad'], gustos=new_node['gustos'], disgusto=new_node['disgusto'], defuncion=new_node['defuncion'])
    
# Extraer el ID del nodo del resultado
    id_nodo_insertado = result_id.single()['id_nodo']

#query para relacionar dos nodos
    query="""
    MATCH (n1:User), (n2:User) WHERE id(n1) = $id_nodo_insertado AND n2.name = $nodo_asignado CREATE (n1)-[r:""" + new_node['relacion'] + """]->(n2)
    """
    result = session.run(query, id_nodo_insertado=id_nodo_insertado, nodo_asignado=new_node['nodo_asignado'], nombre_relacion=new_node['relacion'])

#vuelve a la interfaz y muestra un mensaje de insercion exitosa
    return render_template('interfaz2.html', bandera = bandera)



  return render_template('interfaz2.html', bandera = bandera)



















@app.route('/update')
def interfaz3():
  return render_template('interfaz3.html')


#@app.route('/delete')
#def interfaz4():
#  return render_template('interfaz4.html')



def borrar_nodo_y_relaciones_por_nombre(name):
    try:
        # Imprimir el nombre del nodo antes de borrarlo
        print("Borrando nodo:", name)

        # Construir la consulta Cypher para eliminar las relaciones del nodo
        cypher_query_relaciones = f"MATCH (n:Family_A{{name:'{name}'}})-[r]-() DELETE r"

        # Imprimir la consulta antes de ejecutarla
        print("Consulta Neo4j para eliminar relaciones:", cypher_query_relaciones)

        # Ejecutar la consulta para eliminar relaciones utilizando la sesión directamente
        with driver.session() as session:
            session.run(cypher_query_relaciones)

        # Construir la consulta Cypher para borrar el nodo
        cypher_query_borrar = f"MATCH (n:Family_A{{name:'{name}'}}) DELETE n"

        # Imprimir la consulta antes de ejecutarla
        print("Consulta Neo4j para borrar nodo:", cypher_query_borrar)

        # Ejecutar la consulta para borrar el nodo utilizando la sesión directamente
        with driver.session() as session:
            session.run(cypher_query_borrar)

        print("Nodo y relaciones borradas exitosamente.")
    except Exception as e:
        # Imprimir cualquier error que ocurra durante la ejecución
        print("Error en la ejecución de la consulta:", str(e))


@app.route('/delete', methods=['GET', 'POST'])
def interfaz4():
    bandera = '0'

    if request.method == 'POST' and 'bandera' in request.form:
        if request.form['bandera'] == '1':
            arbol_seleccionado = request.form['arbol']
            nodos_a_borrar = obtener_nodos_relacionados(arbol_seleccionado)
            bandera = request.form['bandera']
            return render_template('interfaz4.html', nodos_a_borrar=nodos_a_borrar, bandera=bandera)

        elif request.form['bandera'] == '2':
            # Obtener el nombre del nodo a borrar
            nodo_a_borrar_nombre = request.form.get('nodo_seleccionado')

            if nodo_a_borrar_nombre:
                # Agregar una impresión de log para verificar el nombre del nodo antes de intentar borrarlo
                print("Nombre del nodo a borrar:", nodo_a_borrar_nombre)

                # Implementar la lógica para borrar el nodo seleccionado por nombre y sus relaciones
                borrar_nodo_y_relaciones_por_nombre(nodo_a_borrar_nombre)

                # Redirigir a la interfaz deseada después de borrar el nodo
                return render_template('interfaz4.html', bandera='2')

    return render_template('interfaz4.html', bandera=bandera)