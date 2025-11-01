from flask import request, jsonify
from app.blueprints.products import bp
from .service import products_sample
@bp.get("/sample")
def sample():
    n = int(request.args.get("n", 10))
    return jsonify(products_sample(n))
