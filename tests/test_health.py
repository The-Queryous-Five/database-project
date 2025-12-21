"""
Tests for health endpoint
Sprint B - Testing without real DB using monkeypatching
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


def test_health_endpoint_structure(client):
    """Test /health returns expected JSON structure (even if DB fails)."""
    
    response = client.get('/health')
    
    # Should return 200 or 503, but always with proper structure
    assert response.status_code in [200, 503]
    data = response.get_json()
    
    # Verify structure exists regardless of DB status
    assert 'api_status' in data
    assert 'db_connected' in data
    assert 'db_vendor' in data
    assert data['api_status'] == 'ok'
    assert isinstance(data['db_connected'], bool)


def test_health_endpoint_db_failure(client, monkeypatch):
    """Test /health returns 503 when DB connection fails."""
    
    # Monkeypatch to raise exception
    def mock_get_conn_fail():
        raise ConnectionError("Database unavailable")
    
    import app.db.db
    monkeypatch.setattr(app.db.db, "get_conn", mock_get_conn_fail)
    
    response = client.get('/health')
    
    assert response.status_code == 503
    data = response.get_json()
    
    assert data['db_connected'] == False
    assert 'errors' in data
    assert len(data['errors']) > 0
