from flask import Flask, request, jsonify

app = Flask(__name__)

# This token must match what you enter in the Meta Dashboard
VERIFY_TOKEN = "your_chosen_secret_token"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta verification step
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        
        # Check if it's a message event
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        # --- EXECUTE YOUR CODE HERE ---
                        msg = value["messages"][0]
                        sender = msg["from"]
                        text = msg.get("text", {}).get("body")
                        print(f"Received '{text}' from {sender}")
                        # ------------------------------
                        
        return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
