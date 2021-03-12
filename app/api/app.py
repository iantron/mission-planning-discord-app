import os

from flask import Flask, Response, jsonify, request

from .errors import errors

from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import airtable

# Set up Discord
client_public_key_path = os.getenv('CLIENT_PUBKEY_FILE')
with open(client_public_key_path, "r") as f:
    CLIENT_PUBLIC_KEY = f.read()

# Set up Airtable
table_api_key_path = os.getenv('TABLE_API_KEY_FILE')
with open(table_api_key_path, "r") as f:
    AIRTABLE_API_KEY = f.read()

# air_plan = airtable.Airtable(AIRTABLE_BASE_KEY, AIR_PLAN_)

# Set up Flask application
app = Flask(__name__)
app.register_blueprint(errors)


# Define Flask Routes
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
        # air_plan.create_flight(data)
        # callsign = data['options']['flight-callsign']
        # task = data['options']['task']
        # airframe = data['options']['airframe']
        # datetime = data['options']['datetime']
        # user_id = data['member']['user']['id']
        # user_nick = data['member']['nick']
        # user_roles = data['member']['roles']
        # if FLIGHT_PLANNER not in user_roles:
            # return jsonify({
                # 'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                # 'data': {
                    # 'content': 'You are not an authorized flight planner. Speak with your game admin.'
                # }
            # })
        # else:
            # air_plan.create_flight( data )
            # return jsonify({
                # 'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                # 'data': {
                    # 'content': 'Flight registered'
                # }
            # })
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Flight registered'
            }
        })
        
        
        
        
        
        
        
        
        
        