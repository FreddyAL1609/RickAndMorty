import requests as requests
from flask import Flask, render_template
from pymongo import MongoClient

# MONGO_URI = "mongodb://localhost"
# client = MongoClient(MONGO_URI)
# db = client['RickAndMortyAPI']
# collection = db['personajes']

# for pagina in range(1, 21):
#     peticion = requests.get(f"https://rickandmortyapi.com/api/character?page={pagina}")
#     datos = peticion.json()
#     #collection.insert_many(datos["results"])
    
    
MONGO_URI = "mongodb://localhost"
client = MongoClient(MONGO_URI)
db = client['RickAndMortyAPI']
collection = db['personajes']

for pagina in range(1, 43):
    peticion = requests.get(f"https://rickandmortyapi.com/api/character?page={pagina}")
    datos = peticion.json()
    #collection.insert_many(datos["results"])

app = Flask(__name__)


@app.route("/")
@app.route("/<int:pagina>")
def examen(pagina=1):
    # Se obtiene la cantidad total de documentos en la colección
    total = collection.count_documents({})
    # Se calcula el número de páginas
    paginas = (total + 19) // 20
    # Se calcula el índice inicial y final para la página solicitada
    inicio = (pagina - 1) * 20
    fin = pagina * 20
    # Se obtienen los documentos de la página solicitada
    todos = collection.find().sort("id", -1).skip(inicio).limit(20)
    # Si la página solicitada es mayor al número de páginas, se redirige a la última página
    if pagina > paginas:
        return redirect(url_for("examen", pagina=paginas))
    # Se devuelve la plantilla de la página
    return render_template("index.html", lista=todos, pagina=pagina, paginas=paginas)


@app.route("/ver/<int:codigo>")
def perfil(codigo):
    perf = collection.find({ "id": codigo })
    return render_template("perfil.html", perfil = perf)

@app.route("/capitulo/<int:capitulo>")
def capitulo(capitulo):
    perf = collection.find({"episode":{"$all":[f'https://rickandmortyapi.com/api/episode/{capitulo}']}})
    return render_template("capitulo.html", capitulo=perf)

