from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Server works"

@app.route("/click")
def click():
    uid = request.args.get("uid", "unknown")
    return f"Click from {uid}"

@app.route("/postback")
def postback():
    uid = request.args.get("subid")
    status = request.args.get("status")
    amount = request.args.get("amount")
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
