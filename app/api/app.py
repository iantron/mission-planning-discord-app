from flask import Flask, Response, jsonify, request

from .errors import errors

from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType

f = open("/run/secrets/client-pubkey", "r")
CLIENT_PUBLIC_KEY = f.read()

app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route("/health")
def health():
    return Response("OK", status=200)

#######################
# Discord Interactions
#######################

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
  if request.json['type'] == InteractionType.APPLICATION_COMMAND:
    data = request.json['data']
    
    if data['name'] == 'hello':
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Hello world'
            }
        })
    elif data['name'] == 'create-flight':
        callsign = data['options']['flight-callsign']
        task = data['options']['task']
        airframe = data['options']['airframe']
        datetime = data['options']['datetime']
        user_id = data['member']['user']['id']
        user_nick = data['member']['nick']
        user_roles = data['member']['roles']
        if FLIGHT_PLANNER not in user_roles:
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': 'You are not an authorized flight planner. Speak with your game admin.'
                }
            })
        else:
            air_plan.create_flight( callsign, task, airframe, datetime, user_id, user_nick )
            return jsonify({
                'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                'data': {
                    'content': 'Flight registered'
                }
            })
            
        
        
        
        
        
        
        
        
        
        