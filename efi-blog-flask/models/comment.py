from datetime import datetime
from app import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_visible = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "author_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat(),
            "is_visible": self.is_visible
        }
