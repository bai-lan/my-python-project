from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"}), 200

@app.route('/about')
def about():
    return jsonify({"version": "1.0", "author": "Bai Lan"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
