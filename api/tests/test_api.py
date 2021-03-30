import os
import time
import json
import pytest
from app.app import create_app
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from flask import Flask, Response, jsonify, request
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType

@pytest.fixture
def signing_key():
    signing_key = SigningKey(bytes.fromhex('543ec69d8f5afe234497f4aa3f656f5d71013bb14361e4b1c235a4e839715a34'))
    return(signing_key)

@pytest.fixture
def verify_key(signing_key):
    verify_key_hex = signing_key.verify_key.encode().hex()
    return(str(verify_key_hex))

@pytest.fixture
def client(verify_key):
    test_config = {}
    test_config["CLIENT_PUBLIC_KEY"] = verify_key
    flask_app = create_app(test_config = test_config)
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client

def test_index(client):
    assert client.get("/").status_code == 200

def test_health(client):
    assert client.get("/health").status_code == 200

def test_ping(signing_key, client):
    timestamp = str(time.time())
    print("Timestamp: ", timestamp)

    payload_dict = {'type': InteractionType.PING }
    print("Data: ", payload_dict)

    message = timestamp.encode() + json.dumps(payload_dict).encode()
    print("Message", message)
    message_signed = signing_key.sign(message)
    print("Message Signature: ", message_signed.signature.hex())

    assert client.post("/interactions",
        json=payload_dict,
        headers={
            'X-Signature-Ed25519': message_signed.signature.hex(),
            'X-Signature-Timestamp': timestamp
        }
    ).status_code == 200
