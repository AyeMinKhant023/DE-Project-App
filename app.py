from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Automated Cloud Security Project</h1>" \
    "<p>✅ AWS server by Patric is Running!</p>" \
    "<p>✅ Database connection is successful!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)