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
  
    # Esto fue modificado 
    if(nombre_nodo_raiz == 'Saúl'):
      cypher_query = f"MATCH (u:User {{name: '{nombre_nodo_raiz}'}})-[]-(x:Family_A) RETURN x"
      resultados = ejecutar_consulta(cypher_query)
      return [registro['x'] for registro in resultados]
    elif(nombre_nodo_raiz == 'Luis'):   
      cypher_query = f"MATCH (u:User {{name: '{nombre_nodo_raiz}'}})-[]-(x:Family_B) RETURN x"
      resultados = ejecutar_consulta(cypher_query)
      return [registro['x'] for registro in resultados]
    else:
      cypher_query = f"MATCH (u:User {{name: '{nombre_nodo_raiz}'}})-[]-(x:Family_C) RETURN x"
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

    return render_template('interfaz2.html', nodos=nodos_relacionados, bandera = bandera, nodo_raiz = arbol_seleccionado)







# Fase 2 escoger el nodo al cual va estar relacionado y su tipo de relación
  if request.method == 'POST' and request.form['bandera'] == '2':
  
    nodo_raiz = request.form['nodo_raiz']
    relacion = request.form['relacion']
    bandera = request.form['bandera']

    if(relacion == 'AMIGO_DE'):
      bandera = '3'
      return render_template('interfaz2.html', bandera = bandera,relacion = relacion, nodo_raiz = nodo_raiz)
    
    elif(relacion == 'PADRE_DE' or relacion == 'CASADO_CON' or relacion == 'PARIENTE_DE'):
      bandera = '4'
      nodos_relacionados = obtener_nodos_relacionados(nodo_raiz)

      return render_template('interfaz2.html', bandera = bandera,relacion = relacion, nodo_raiz = nodo_raiz, nodos_relacionados = nodos_relacionados)
   
    return render_template('interfaz2.html', bandera = bandera,relacion = relacion)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
# Fase 3 inserta nuevo nodo que tiene relación directa de ''AMIGO_DE'' con nodo raiz  
  if request.method == 'POST' and request.form['bandera'] == '4' and request.form['relacion'] == 'AMIGO_DE':
    
    new_node = {
      'nombre': request.form['nombre'],
      'apellido': request.form['apellido'],
      'edad': request.form['edad'],
      'actividad':request.form['actividad'],
      'gustos': [request.form['gusto1'],request.form['gusto2']],
      'disgusto': request.form['disgusto'],
      'defuncion': request.form['defuncion'],
      'nodo_asignado': request.form['nodo_raiz'], 
      'relacion':request.form['relacion'],
    }
    # query para crea el nodo
    query = """
    CREATE (:Amigo {
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
    result = session.run(query, name=new_node['nombre'], apellido=new_node  ['apellido'], edad=new_node['edad'], actividad=new_node['actividad'],   gustos=new_node['gustos'], disgusto=new_node['disgusto'], defuncion=new_node  ['defuncion'])
    
     # Obtiene el id del nodo creado para relacionar
    query_obtener_id = """
      MATCH (a:Amigo {name: $nombre, apellido: $apellido, edad: $edad, actividad:      $actividad, gustos: $gustos, disgusto: $disgusto, defuncion: $defuncion})
      RETURN id(a) AS id_nodo
      """
    result_id = session.run(query_obtener_id, nombre=new_node['nombre'],  apellido=new_node['apellido'], edad=new_node['edad'], actividad=new_node ['actividad'], gustos=new_node['gustos'], disgusto=new_node['disgusto'],   defuncion=new_node['defuncion'])
    
    # Extraer el ID del nodo del resultado
    id_nodo_insertado = result_id.single()['id_nodo']
    
    #query para relacionar dos nodos
    query="""
      MATCH (a:Amigo), (n:User) WHERE id(a) = $id_nodo_insertado AND n.name =  $nodo_asignado CREATE (a)-[r:""" + new_node['relacion'] + """]->(n)
      """
    result = session.run(query, id_nodo_insertado=id_nodo_insertado, nodo_asignado=new_node['nodo_asignado'], nombre_relacion=new_node['relacion'])
    
    bandera = 'exito'
    #vuelve a la interfaz y muestra un mensaje de insercion exitosa
    return render_template('interfaz2.html', bandera = bandera)
  
  
  
  
  
#Fase 4 para el caso de relacion PADRE_DE, CASADO_CON, PARIENTE_DE  
  if (request.method == 'POST' and request.form['bandera'] == '5') and (request.form['relacion'] == 'PADRE_DE' or request.form['relacion'] == 'PARIENTE_DE' or request.form['relacion'] == 'CASADO_CON'):
    
    nodo_raiz = request.form['nodo_raiz']
    nodo_asignado = request.form['nodo_asignado']
    relacion = request.form['relacion']
    
    return render_template('interfaz2.html', bandera = request.form['bandera'], nodo_raiz = nodo_raiz, nodo_asignado = nodo_asignado, relacion = relacion)
    
    
  if request.method == 'POST' and request.form['bandera'] == '6':
    
    nodo_raiz = request.form['nodo_raiz']
    
    new_node = {
      'nombre': request.form['nombre'],
      'apellido': request.form['apellido'],
      'edad': request.form['edad'],
      'actividad':request.form['actividad'],
      'gustos': [request.form['gusto1'],request.form['gusto2']],
      'disgusto': request.form['disgusto'],
      'defuncion': request.form['defuncion'],
      'nodo_asignado': request.form['nodo_asignado'], 
      'relacion':request.form['relacion'],
    }
    
    if nodo_raiz == 'Saúl':
      # query para crea el nodo
      query = """
      CREATE (:Family_A {
        name: $name,
        apellido: $apellido,
        edad: $edad,
        actividad: $actividad,
        gustos: $gustos,
        disgusto: $disgusto,
        defuncion: $defuncion
      })
      """
     
    elif nodo_raiz == 'Luis':
      # query para crea el nodo
      query = """
      CREATE (:Family_B {
        name: $name,
        apellido: $apellido,
        edad: $edad,
        actividad: $actividad,
        gustos: $gustos,
        disgusto: $disgusto,
        defuncion: $defuncion
      })
      """
      
    else:
      # query para crea el nodo
      query = """
      CREATE (:Family_C {
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
    result = session.run(query, name=new_node['nombre'], apellido=new_node  ['apellido'], edad=new_node['edad'], actividad=new_node['actividad'],   gustos=new_node['gustos'], disgusto=new_node['disgusto'], defuncion=new_node  ['defuncion'])
    
      # Obtiene el id del nodo creado para relacionar
    if nodo_raiz == 'Saúl':
      query_obtener_id = """
      MATCH (f:Family_A {name: $nombre, apellido: $apellido, edad: $edad, actividad:      $actividad, gustos: $gustos, disgusto: $disgusto, defuncion: $defuncion})
      RETURN id(f) AS id_nodo
      """
    elif nodo_raiz == 'Luis':
      query_obtener_id = """
      MATCH (f:Family_B {name: $nombre, apellido: $apellido, edad: $edad, actividad:      $actividad, gustos: $gustos, disgusto: $disgusto, defuncion: $defuncion})
      RETURN id(f) AS id_nodo
      """
    else:
      query_obtener_id = """
      MATCH (f:Family_C {name: $nombre, apellido: $apellido, edad: $edad, actividad:      $actividad, gustos: $gustos, disgusto: $disgusto, defuncion: $defuncion})
      RETURN id(f) AS id_nodo
      """
    #ejecuta la query  
    result_id = session.run(query_obtener_id, nombre=new_node['nombre'],  apellido=new_node['apellido'], edad=new_node['edad'], actividad=new_node ['actividad'], gustos=new_node['gustos'], disgusto=new_node['disgusto'],   defuncion=new_node['defuncion'])

      # Extraer el ID del nodo del resultado
    id_nodo_insertado = result_id.single()['id_nodo']
    
    if nodo_raiz == 'Saúl' and new_node['nodo_asignado'] == 'Saúl':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_A), (n:User) WHERE id(f) = $id_nodo_insertado AND n.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(n)
      """
    elif nodo_raiz == 'Luis' and new_node['nodo_asignado'] == 'Luis':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_B), (n:User) WHERE id(f) = $id_nodo_insertado AND n.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(n)
      """
    elif nodo_raiz == 'Víctor' and new_node['nodo_asignado'] == 'Víctor':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_C), (n:User) WHERE id(f) = $id_nodo_insertado AND n.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(n)
      """
    elif nodo_raiz == 'Saúl' and new_node['nodo_asignado'] != 'Saúl':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_A), (f2:Family_A) WHERE id(f) = $id_nodo_insertado AND f2.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(f2)
      """
    elif nodo_raiz == 'Luis' and new_node['nodo_asignado'] != 'Luis':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_B), (f2:Family_B) WHERE id(f) = $id_nodo_insertado AND f2.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(f2)
      """
    elif nodo_raiz == 'Víctor' and new_node['nodo_asignado'] != 'Víctor':
      #query para relacionar dos nodos
      query="""
      MATCH (f:Family_C), (f2:Family_C) WHERE id(f) = $id_nodo_insertado AND f2.name =  $nodo_asignado CREATE (f)-[r:""" + new_node['relacion'] + """]->(f2)
      """    
      
    result = session.run(query, id_nodo_insertado=id_nodo_insertado, nodo_asignado=new_node['nodo_asignado'], nombre_relacion=new_node['relacion'])
    
    #vuelve a la interfaz y muestra un mensaje de insercion exitosa
    return render_template('interfaz2.html', bandera = 'exito')
  
  
  
  #Retorna al inicio      
  return render_template('interfaz2.html', bandera = bandera)

  
















@app.route('/update')
def interfaz3():
  return render_template('interfaz3.html')


@app.route('/delete')
def interfaz4():
  return render_template('interfaz4.html')