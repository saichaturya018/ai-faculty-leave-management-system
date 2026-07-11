from flask import Flask
from flask_cors import CORS
from routes.leave import leave_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(leave_bp)

if __name__ == "__main__":
    app.run(debug=True)