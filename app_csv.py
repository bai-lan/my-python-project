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
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.rsplit('.', 1)[1].lower() == 'csv':
            try:
                data = pd.read_csv(file_path)
                for index, row in data.iterrows():
                    wine_data = row.to_dict()
                    wine = RedWine(**wine_data)
                    db.session.add(wine)
                db.session.commit()
                return jsonify({"message": "Red wines added successfully."}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
