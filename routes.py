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
@app.route('/create')
def interfaz2():
  return render_template('interfaz2.html')

@app.route('/update')
def interfaz3():
  return render_template('interfaz3.html')


@app.route('/delete')
def interfaz4():
  return render_template('interfaz4.html')