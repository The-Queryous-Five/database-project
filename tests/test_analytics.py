"""
Tests for analytics endpoints
Sprint B - Testing complex SQL queries without real DB
"""

import pytest
from app.app import create_app


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_revenue_by_category_validates_limit(client, monkeypatch):
    """Test revenue-by-category validates limit parameter."""
    
    # Mock query function
    def mock_query_all(sql, params=None):
        return []
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    # Test invalid limit (too high)
    response = client.get('/analytics/revenue-by-category?limit=200')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] == False
    assert 'limit' in data['error'].lower()
    
    # Test invalid limit (negative)
    response = client.get('/analytics/revenue-by-category?limit=-5')
    assert response.status_code == 400


def test_revenue_by_category_returns_expected_schema(client, monkeypatch):
    """Test revenue-by-category returns correct JSON structure."""
    
    # Mock data
    mock_data = [
        {
            "category_name": "electronics",
            "items_sold": 100,
            "distinct_orders": 80,
            "total_revenue": 5000.50,
            "avg_item_price": 50.00
        }
    ]
    
    def mock_query_all(sql, params=None):
        return mock_data
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    response = client.get('/analytics/revenue-by-category?limit=10')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['ok'] == True
    assert 'params' in data
    assert 'data' in data
    assert data['params']['limit'] == 10
    assert len(data['data']) == 1
    assert data['data'][0]['category_name'] == 'electronics'


def test_top_sellers_validates_limit(client, monkeypatch):
    """Test top-sellers validates limit parameter."""
    
    def mock_query_all(sql, params=None):
        return []
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    response = client.get('/analytics/top-sellers?limit=150')
    assert response.status_code == 400


def test_top_sellers_returns_expected_schema(client, monkeypatch):
    """Test top-sellers returns correct JSON structure."""
    
    mock_data = [
        {
            "seller_id": "abc123",
            "seller_city": "Sao Paulo",
            "seller_state": "SP",
            "order_count": 50,
            "items_sold": 75,
            "total_revenue": 3500.00,
            "avg_item_price": 46.67
        }
    ]
    
    def mock_query_all(sql, params=None):
        return mock_data
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    response = client.get('/analytics/top-sellers?limit=10')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['ok'] == True
    assert 'seller_id' in data['data'][0]
    assert 'total_revenue' in data['data'][0]


def test_review_vs_delivery_validates_min_reviews(client, monkeypatch):
    """Test review-vs-delivery validates min_reviews parameter."""
    
    def mock_query_all(sql, params=None):
        return []
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    # Test invalid (too high)
    response = client.get('/analytics/review-vs-delivery?min_reviews=5000')
    assert response.status_code == 400
    
    # Test invalid (negative)
    response = client.get('/analytics/review-vs-delivery?min_reviews=0')
    assert response.status_code == 400


def test_order_funnel_returns_data(client, monkeypatch):
    """Test order-funnel returns status breakdown."""
    
    mock_data = [
        {
            "order_status": "delivered",
            "order_count": 96478,
            "avg_delivery_days": 12.5,
            "avg_approval_days": 0.5
        },
        {
            "order_status": "shipped",
            "order_count": 1107,
            "avg_delivery_days": None,
            "avg_approval_days": 0.4
        }
    ]
    
    def mock_query_all(sql, params=None):
        return mock_data
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all)
    
    response = client.get('/analytics/order-funnel')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['ok'] == True
    assert len(data['data']) == 2
    assert data['data'][0]['order_status'] == 'delivered'


def test_analytics_endpoint_db_error_handling(client, monkeypatch):
    """Test analytics endpoints return 503 on DB failure."""
    
    def mock_query_all_fail(sql, params=None):
        raise ConnectionError("Database connection failed")
    
    monkeypatch.setattr("app.routes.analytics._query_all", mock_query_all_fail)
    
    response = client.get('/analytics/revenue-by-category?limit=10')
    assert response.status_code == 503
    
    data = response.get_json()
    assert data['ok'] == False
    assert 'error' in data
