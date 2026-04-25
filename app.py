from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Automated Cloud Security Project</h1>" \
    "<p>AWS server by Patric is Running!</p>"

if __name__ == '__main__':
    # We use 0.0.0.0 so it listens on the public IP, not just locally
    app.run(host='0.0.0.0', port=5000)