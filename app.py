from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
import pandas as pd
import os
from redWine import app, db, RedWine  # Import the Flask app, db, and RedWine model from redWine

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/red-wines/upload', methods=['POST'])
def upload_wines():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    try:
        for wine_data in data:
            wine = RedWine(**wine_data)
            db.session.add(wine)
        db.session.commit()
        return jsonify({"message": "Red wines added successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
