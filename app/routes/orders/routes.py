from flask import Blueprint, request, jsonify

# Az önce yazdığımız service fonksiyonunu import ediyoruz
from .service import get_orders_by_customer 

# 'orders' adında yeni bir Blueprint (Flask modülü) oluşturuyoruz
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

#
# Burası senin Hafta 3 görevin olan yeni endpoint:
#
@orders_bp.route('/by-customer/<string:customer_id>', methods=['GET'])
def list_orders_by_customer(customer_id):
    """
    Belirli bir müşterinin siparişlerini listeler.
    GET /orders/by-customer/1234567890?limit=10
    """
    
    # --- Validasyon (Görev 2) ---
    limit_str = request.args.get('limit', '10') # limit'i al, yoksa 10 say

    try:
        limit = int(limit_str)
        if not (1 <= limit <= 50):
            return jsonify({"error": "limit must be between 1 and 50"}), 422
    except ValueError:
        return jsonify({"error": "limit must be a valid integer"}), 422
    # --- Validasyon Sonu ---

    # Servis fonksiyonunu çağır
    orders = get_orders_by_customer(customer_id, limit)
    
    # Sonucu JSON olarak dön
    return jsonify(orders), 200

#
# NOT: Bu 'orders_bp'nin ana app/app.py dosyasında register edilmesi gerekir.
# Eğer edilmediyse, app/app.py'a gidip
# from app.routes.orders.routes import orders_bp
# ...
# app.register_blueprint(orders_bp)
# satırlarını eklemeniz gerekebilir.
#