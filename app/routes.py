import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Submission

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or 'name' not in data or 'score' not in data:
        return jsonify({"error": "Missing 'name' or 'score' in request body"}), 400

    try:
        new_submission = Submission(name=data['name'], score=data['score'])
        
        db.session.add(new_submission)
        db.session.commit()
        
        return jsonify({
            "message": "Data submitted successfully!",
            "id": new_submission.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    try:
        all_submissions = Submission.query.all()
        results = [submission.to_dict() for submission in all_submissions]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0", port=5000)