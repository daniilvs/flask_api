from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    score = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'timestamp': self.timestamp.isoformat()
        }
        