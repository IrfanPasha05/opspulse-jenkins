from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "OpsPulse",
        "version": "1.0"
    })


@app.route("/api/status")
def api_status():
    return jsonify({
        "application": "OpsPulse",
        "environment": "Jenkins-EC2",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
