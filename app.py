from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Project Alpha: Live!</h1><p>The EC2 is running and Flask is working.</p>"

if __name__ == '__main__':
    # We use 0.0.0.0 so it listens on the public IP, not just locally
    app.run(host='0.0.0.0', port=5000)