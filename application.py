from flask import Flask, request, jsonify
from fmcsa_utils import verify_mc
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

application = Flask(__name__)  # changed from app

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOOKINGS_FILE = 'bookings.json'

@application.route('/check-key')
def check_key():
    return jsonify({"FMCSA_API_KEY": os.getenv("FMCSA_API_KEY")})

@application.route('/verify-mc', methods=['GET'])
def verify_mc_route():
    mc_number = request.args.get('mc_number')
    if not mc_number:
        return jsonify({'error': 'Missing mc_number parameter'}), 400

    logger.info(f"Verifying MC number: {mc_number}")
    result = verify_mc(mc_number)
    return jsonify(result)


@application.route('/get-load', methods=['GET', 'POST'])
def get_load():
    # Try query param first
    load_id = request.args.get('load_id')

    # If not found, try from JSON body
    if not load_id and request.is_json:
        data = request.get_json()
        load_id = data.get("load_id")

    if not load_id:
        return jsonify({"error": "Missing load_id"}), 400

    with open('loads_db.json') as f:
        loads = json.load(f)

    # Use str() to ensure match
    load = next((l for l in loads if str(l['load_id']) == str(load_id)), None)
    
    if not load:
        return jsonify({
            "found": False,
            "error": "Load not found",
            "load_id_received": load_id,
            "available_ids": [l['load_id'] for l in loads]
        }), 404

    pitch = pitch_load(load)

    return jsonify({
        "found": True,
        "load": load,
        "pitch": pitch
    })


def pitch_load(load):
    return (
        f"It picks up in {load['origin']} on {load['pickup_datetime']}, and delivers to {load['destination']} by {load['delivery_datetime']}. "
        f"It’s around {load['weight']} lbs, freight of {load['commodity_type']}, and we’ll need a {load['equipment_type']}, at least {load['dimensions']} big. "
        f"I’m asking ${load['loadboard_rate']} on this one."
    )


@application.route('/book-load', methods=['POST'])
def book_load():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    logger.info(f"Received booking data: {data}")

    # Load existing bookings or initialize empty list
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r') as f:
            bookings = json.load(f)
    else:
        bookings = []

    bookings.append(data)

    # Save updated bookings to file
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=2)

    return jsonify({"status": "success", "message": "Booking recorded"}), 201


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)
