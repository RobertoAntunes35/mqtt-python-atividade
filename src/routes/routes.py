from flask import jsonify, Blueprint, request, json, render_template
from src.database.model.model import db, Temperatura, Umidade, Solo
routes = Blueprint("routes", __name__)

# Home
@routes.route("/")
def home():
    return render_template('index.html')

@routes.route("/atualizar-dados-temp", methods=["GET", "POST"])
def atualiza_dados():
    dados = []
    temps = Temperatura.query.all()
    for temp in temps:
        dictTemp = {
            'id':temp.id,
            'local':temp.local,
            'value':temp.value
        } 
        dados.append(dictTemp)

    print(dados)
    return jsonify(dados)


@routes.route("/api-roberto/v1/create-new-data/<type>", methods=["POST"])
def temperatura_create(type):
    from main import mqtt
    new_data = None
    topic = None
    data = request.form
    if request.method == "POST":
        if (type == "temp"):
            topic = "listen_temp"
            new_data = Temperatura(
                local=data["local"],
                value=data["value"]
            )
        
        elif (type == "umid"):
            topic = "listen_temp"
            new_data = Umidade(
                local=data["local"],
                value=data["value"]
            ) 

        elif (type == "solo"):
            topic = "listen_temp"
            new_data = Solo(
                local=data["local"],
                value=data["value"]
            )
        try:
            db.session.add(new_data)
            db.session.commit()
            mqtt.publish(f"topic/{topic}", json.dumps(data))
            return jsonify({
                "message":"Temperatura adicionada com sucesso."
            }), 201

        except Exception as ex:
            print(f"Houve um erro ao realizar a inclusão dos dados. \nErro: {ex}")
            return jsonify({
                "error":"erro ao realizar adicionar a temperatura.",
                "message_error":str(ex)
            }), 400

