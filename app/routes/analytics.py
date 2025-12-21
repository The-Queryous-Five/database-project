from flask import Blueprint, jsonify, request
from app.db import db
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

bp_analytics = Blueprint("analytics", __name__)


def _decimal_to_float(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def _query_all(sql, params=None):
    """Execute query and return list of dicts."""
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            return [dict(zip(cols, row)) for row in rows]


@bp_analytics.get("/analytics/revenue-by-category")
def revenue_by_category():
    """
    Complex query: Multi-table join + group by + order by
    
    Joins: order_items + products + orders + categories (if available)
    Computes: total_revenue, items_sold, distinct_orders per category
    """
    try:
        limit = request.args.get("limit", 10, type=int)
        if limit < 1 or limit > 100:
            return jsonify({"ok": False, "error": "limit must be between 1 and 100"}), 400
        
        # Multi-table join with aggregations
        sql = """
        SELECT
            COALESCE(p.product_category_name, 'Unknown') AS category_name,
            COUNT(*) AS items_sold,
            COUNT(DISTINCT oi.order_id) AS distinct_orders,
            ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
            ROUND(AVG(oi.price), 2) AS avg_item_price
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY p.product_category_name
        ORDER BY total_revenue DESC
        LIMIT %s
        """
        
        results = _query_all(sql, (limit,))
        
        return jsonify({
            "ok": True,
            "params": {"limit": limit},
            "data": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in revenue-by-category: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503


@bp_analytics.get("/analytics/top-sellers")
def top_sellers():
    """
    Complex query: Join + group by + distinct + sorting
    
    Joins: order_items + sellers + orders
    Computes: total_revenue, order_count, avg_item_price per seller
    """
    try:
        limit = request.args.get("limit", 10, type=int)
        if limit < 1 or limit > 100:
            return jsonify({"ok": False, "error": "limit must be between 1 and 100"}), 400
        
        sql = """
        SELECT
            s.seller_id,
            s.seller_city,
            s.seller_state,
            COUNT(DISTINCT oi.order_id) AS order_count,
            COUNT(*) AS items_sold,
            ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
            ROUND(AVG(oi.price), 2) AS avg_item_price
        FROM order_items oi
        JOIN sellers s ON s.seller_id = oi.seller_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY s.seller_id, s.seller_city, s.seller_state
        ORDER BY total_revenue DESC
        LIMIT %s
        """
        
        results = _query_all(sql, (limit,))
        
        return jsonify({
            "ok": True,
            "params": {"limit": limit},
            "data": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in top-sellers: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503


@bp_analytics.get("/analytics/review-vs-delivery")
def review_vs_delivery():
    """
    Complex query: Subquery/aggregation + derived metrics + HAVING clause
    
    Computes per seller:
    - avg_review_score
    - avg_delivery_days (delivered - purchase)
    - Filters out low-sample groups with HAVING
    """
    try:
        min_reviews = request.args.get("min_reviews", 50, type=int)
        if min_reviews < 1 or min_reviews > 1000:
            return jsonify({"ok": False, "error": "min_reviews must be between 1 and 1000"}), 400
        
        sql = """
        SELECT
            s.seller_id,
            s.seller_city,
            s.seller_state,
            COUNT(DISTINCT r.review_id) AS review_count,
            ROUND(AVG(r.review_score), 2) AS avg_review_score,
            ROUND(AVG(TIMESTAMPDIFF(DAY, o.order_purchase_timestamp, o.order_delivered_customer_date)), 1) AS avg_delivery_days
        FROM order_items oi
        JOIN sellers s ON s.seller_id = oi.seller_id
        JOIN orders o ON o.order_id = oi.order_id
        LEFT JOIN order_reviews r ON r.order_id = o.order_id
        WHERE o.order_status = 'delivered'
          AND o.order_delivered_customer_date IS NOT NULL
        GROUP BY s.seller_id, s.seller_city, s.seller_state
        HAVING COUNT(DISTINCT r.review_id) >= %s
        ORDER BY avg_review_score DESC, avg_delivery_days ASC
        LIMIT 20
        """
        
        results = _query_all(sql, (min_reviews,))
        
        return jsonify({
            "ok": True,
            "params": {"min_reviews": min_reviews},
            "data": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in review-vs-delivery: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503


@bp_analytics.get("/analytics/order-funnel")
def order_funnel():
    """
    Complex query: Conditional aggregation
    
    Returns counts of orders by status and avg durations between milestones
    """
    try:
        sql = """
        SELECT
            order_status,
            COUNT(*) AS order_count,
            ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)), 1) AS avg_delivery_days,
            ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_approved_at)), 1) AS avg_approval_days
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC
        """
        
        results = _query_all(sql)
        
        return jsonify({
            "ok": True,
            "params": {},
            "data": results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in order-funnel: {e}")
        return jsonify({"ok": False, "error": str(e)}), 503
