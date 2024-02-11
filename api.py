from neo4j import GraphDatabase
from flask import Flask , request, jsonify, redirect, render_template
user = "neo4j"
password = "AKXvKuq9x2ujefjpD2QVhkl7iJynyqpQEu3DTRVgs-8"
uri = "neo4j+s://f9bb7262.databases.neo4j.io"

driver = GraphDatabase.driver(uri=uri, auth=(user, password))
session = driver.session()
#query = """
#create (:User{name:'Víctor', apellido: 'Rojas' ,edad:20, actividad:'Estudiante', 
#gustos:['Tecnologías', 'Autos'], disgusto:'Motos', defuncion: 'No'})
#"""

#session.run(query)
#print('Insercion exitosa')

query2 = "match (n) return n"

with driver.session() as session:
    resultados = session.run(query2)

    # Procesar los resultados
    for registro in resultados:
        print(registro)

print('impresion exitosa')