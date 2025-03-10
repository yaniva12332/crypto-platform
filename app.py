from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from binance.client import Client

app = Flask(__name__)
CORS(app)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Binance API
API_KEY = "ppb14bFJdk1ZOBN0zPtIAKwPTrgflY7WE3DPAti3Lur0lcUdp7W1d9ZLaI3BCQnQ"
API_SECRET = "dMZiAJgcbM19FAEDxvDX8V7OIQkx8udZQUoOqnmOeUuTE3nKv5yMMDsjZ8crUOTc"
client = Client(api_key=API_KEY, api_secret=API_SECRET)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    subscription_status = db.Column(db.Boolean, server_defualt="0", nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/get_price', methods=['GET'])
def get_price():
    symbol = request.args.get('symbol', 'BTCUSDT')
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return jsonify({"symbol": symbol, "price": ticker['price']})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")
    app.run(debug=True, port=5000)
