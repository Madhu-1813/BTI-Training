from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({
        "message": "Python application is running on ECS Fargate"
    })

@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello from Python container"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)