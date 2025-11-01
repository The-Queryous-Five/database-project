from flask import jsonify
from app.blueprints.reviews import bp
from .service import recent_reviews
@bp.get("/recent")
def recent():
    return jsonify(recent_reviews())
