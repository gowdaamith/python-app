from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    version = os.getenv("APP_VERSION", "v1.0")
    env = os.getenv("ENVIRONMENT", "dev")
    return f"Hello from Python App! Version: {version} | Environment: {env}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
