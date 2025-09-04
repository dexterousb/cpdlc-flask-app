from flask import Flask, jsonify, render_template, request
from datetime import datetime
import time

app = Flask(__name__)

# Constant for error message
INVALID_DATA_ERROR = "Invalid data"

# Mock ATC responses, the taxi clearance message will remain unchanged
ATC_RESPONSES = {
    "expected_taxi_clearance": "TAXI VIA C, C1, B, B1. HOLDSHORT RWY 25R",
    "engine_startup": "ENGINE STARTUP APPROVED",
    "pushback": "PUSHBACK APPROVED",
    "taxi_clearance": "TAXI CLEARANCE GRANTED",
    "de_icing": "DE-ICING NOT REQUIRED"
}

# The taxi clearance message will not be altered
TAXI_CLEARANCE_MESSAGE = "TAXI VIA C, C1, B, B1. HOLDSHORT RWY 25R"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Log route
@app.route('/log', methods=['GET'])
def log_action():
    time.sleep(2)  # Simulate delay
    response = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "message": "ATC has acknowledged your log request. Proceed with actions.",
    }
    app.logger.info("Log request acknowledged.")
    return jsonify(response)

# Handle ATC requests
@app.route('/request/<action>', methods=['GET'])
def request_action(action):
    if action in ATC_RESPONSES:
        response = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action": action.replace("_", " ").title(),
            "message": ATC_RESPONSES[action],
            "status": "open"
        }
        app.logger.info(f"Action requested: {action} - Response: {response}")
        return jsonify(response)
    else:
        app.logger.warning(f"Invalid action requested: {action}")
        return jsonify({"error": "Invalid action"}), 400

# Load taxi clearance
@app.route('/load', methods=['POST'])
def load_taxi_clearance():
    data = request.get_json()
    if data and data.get("requestType") == "loadTaxiClearance":
        time.sleep(1)  # Simulate processing delay
        response = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": "Taxi clearance data loaded successfully.",
        }
        app.logger.info("Taxi clearance data loaded.")
        return jsonify(response)
    else:
        app.logger.error("Invalid request type for loading taxi clearance.")
        return jsonify({"error": INVALID_DATA_ERROR}), 400

# Update action status
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    if "action" in data and "status" in data:
        action = data["action"]
        status = data["status"]
        time.sleep(1)  # Simulate status update
        app.logger.info(f"Status updated for {action}: {status}")
        return jsonify({"message": "Status updated successfully", "new_status": status})

    app.logger.error(f"Invalid data for status update: {data}")
    return jsonify({"error": INVALID_DATA_ERROR}), 400

# Handle Wilco, Standby, and Unable actions
@app.route('/action/<button>', methods=['POST'])
def handle_action(button):
    time.sleep(1)  # Simulate processing delay
    valid_buttons = ["wilco", "standby", "unable"]
    if button in valid_buttons:
        response = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": f"ATC has acknowledged your '{button.upper()}' action.",
        }
        app.logger.info(f"Button '{button.upper()}' action processed.")
        return jsonify(response)
    else:
        app.logger.warning(f"Invalid button action attempted: {button}")
        return jsonify({"error": "Invalid button action"}), 400

# Execute endpoint - does not affect the taxi clearance message
@app.route('/execute', methods=['POST'])
def execute_action():
    data = request.get_json()
    if data:
        time.sleep(1)  # Simulate processing delay
        response = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": TAXI_CLEARANCE_MESSAGE,
        }
        app.logger.info("Execute action processed.")
        return jsonify(response)
    else:
        app.logger.error("Invalid data for execute action.")
        return jsonify({"error": INVALID_DATA_ERROR}), 400

# Cancel endpoint - does not affect the taxi clearance message
@app.route('/cancel', methods=['POST'])
def cancel_action():
    data = request.get_json()
    if data:
        time.sleep(1)  # Simulate processing delay
        response = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": "CANCEL action received, but taxi clearance remains unchanged: " + TAXI_CLEARANCE_MESSAGE,
        }
        app.logger.info("Cancel action processed.")
        return jsonify(response)
    else:
        app.logger.error("Invalid data for cancel action.")
        return jsonify({"error": INVALID_DATA_ERROR}), 400

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    app.logger.warning("Attempted access to a non-existent endpoint.")
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# Utility route for health check
@app.route('/health', methods=['GET'])
def health_check():
    app.logger.info("Health check performed.")
    return jsonify({"status": "OK", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

if __name__ == '__main__':
    app.run(debug=True)
