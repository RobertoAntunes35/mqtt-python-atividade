import json 
import eventlet

from flask import Flask 

from src.database.model.model import db
from src.routes.routes import routes
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5
app.register_blueprint(routes)
db.init_app(app)
mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('topic/listen_temp')
    socketio.emit('mqtt_connection_status', {'message': 'Connected to MQTT broker'})

@mqtt.on_message()
def handle_message(client, userdata, message):
    print(f'Recebido mensagem no topico {message.topic}: {message.payload.decode()}')

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic/listen_temp'], data['message'])

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic/listen_temp'])
    socketio.emit('subscription_status', {'message': f'Subscribed to topic: {data["topic"]}'})

@socketio.on('unsubscribe')
def handle_unsubscribe(json_str):
    data = json.loads(json_str)
    mqtt.unsubscribe(data['topic'])
    socketio.emit('subscription_status', {'message': f'Unsubscribed from topic: {data["topic"]}'}) 
    

with app.app_context():
    db.create_all()