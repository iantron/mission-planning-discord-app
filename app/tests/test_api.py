import os
import datetime
import pytest
from api.app import app
from nacl.signing import SigningKey

client_public_key_path = './secrets/discord-public-key.secret'
os.environ['CLIENT_PUBKEY_FILE'] = client_public_key_path
table_api_key_path = './secrets/airtable-api-key.secret'
os.environ['TABLE_API_KEY_FILE'] = table_api_key_path

@pytest.fixture
def client():
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    verify_key_bytes = verify_key.encode()
    
    with open(client_public_key_path, 'w') as f:
        f.write(verify_key_bytes)
    
    with app.test_client() as client:
        with client.session_transaction as sess:
            sess['signing_key'] = signing_key
            
        yield client


def test_index(client):
    assert client.get("/").status_code == 200


def test_health(client):
    assert client.get("/health").status_code == 200

def test_ping(client):
    with client.session_transaction as sess:
        signing_key = sess['signing_key']
    
    timestamp = datetime.datetime.now()
    
    data = jsonify({
                    'type': InteractionType.PING
                })

    message = timestamp.encode + data.encode
    message_signed = signing_key.sign(message)
    
    assert client.post("/interactions",
        json=data,
        headers={
            'X-Signature-Ed25519' = message_signed.signature,
            'X-Signature-Timestamp' = timestamp
        }
    ).status_code == 200