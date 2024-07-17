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

#delete a specific red wine entry from the database by its ID
@app.route('/red-wines/<int:wine_id>', methods=['DELETE'])
def delete_wine(wine_id):
    wine = RedWine.query.get(wine_id)
    if wine is None:
        return jsonify({"error": "Red wine not found"}), 404
    try:
        db.session.delete(wine)
        db.session.commit()
        return jsonify({"message": "Red wine deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#to retrieve red wine data from the RedWine table in your PostgreSQL database.
@app.route('/red-wines', methods=['GET'])
def get_wines():
    try:
        wines = RedWine.query.all()
        wine_list = []
        for wine in wines:
            wine_data = {
                'id': wine.id,
                'name': wine.name,
                'year': wine.year,
                'region': wine.region,
                'price': wine.price,
                'fixed_acidity': wine.fixed_acidity,
                'volatile_acidity': wine.volatile_acidity
            }
            wine_list.append(wine_data)
        app.logger.info(f"Fetched {len(wine_list)} wines successfully.")
        return jsonify({"red_wines": wine_list}), 200
    except Exception as e:
        app.logger.error(f"Error fetching wines: {str(e)}")
        return jsonify({"error": str(e)}), 500

#This endpoint is used to update a specific wine record identified by wine_id.    
@app.route('/red-wines/<int:wine_id>', methods=['PUT'])
def update_wine(wine_id):
    wine = RedWine.query.get(wine_id)
    if not wine:
        return jsonify({"error": "Wine not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        wine.name = data.get('name', wine.name)
        wine.year = data.get('year', wine.year)
        wine.region = data.get('region', wine.region)
        wine.price = data.get('price', wine.price)
        wine.fixed_acidity = data.get('fixed_acidity', wine.fixed_acidity)
        wine.volatile_acidity = data.get('volatile_acidity', wine.volatile_acidity)

        db.session.commit()
        return jsonify({"message": "Wine updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#to update only certain fields of an existing resource without requiring the entire resource to be provided.
# @app.route('/red-wines/<int:wine_id>', methods=['PATCH'])
# def update_wine(wine_id):
#     wine = RedWine.query.get(wine_id)
#     if not wine:
#         return jsonify({"error": "Wine not found"}), 404

#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     try:
#         for key, value in data.items():
#             if hasattr(wine, key):
#                 setattr(wine, key, value)

#         db.session.commit()
#         return jsonify({"message": "Wine updated successfully"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
