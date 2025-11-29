#!/usr/bin/env python3
"""
Test script for Customers Geo Analytics endpoints.

Usage:
    python test_geo_analytics.py

Prerequisites:
    - Flask app should be running: flask --app app/app.py run
    - Database should be populated with customers and geo_zip data
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:5000"

def print_test(name: str):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")

def print_result(response: requests.Response, expected_status: int = None):
    """Print response details."""
    print(f"Status: {response.status_code} (expected: {expected_status or 'any'})")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response (text): {response.text}")
    if expected_status and response.status_code != expected_status:
        print(f"❌ FAILED: Expected {expected_status}, got {response.status_code}")
        return False
    elif expected_status:
        print(f"✅ PASSED")
        return True
    return True

def test_health():
    """Test health endpoint."""
    print_test("Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_result(response, 200)

def test_customers_by_city_valid():
    """Test /customers/by-city with valid parameters."""
    print_test("Customers by City - Valid Request")
    params = {
        "state": "SP",
        "city": "sao_paulo",
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/customers/by-city", params=params)
    success = print_result(response, 200)
    if success and response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ Found {len(data)} customers")
            print(f"   Sample: customer_id={data[0].get('customer_id')}, city={data[0].get('city')}, state={data[0].get('state')}")
    return success

def test_customers_by_city_missing_state():
    """Test /customers/by-city with missing state parameter."""
    print_test("Customers by City - Missing State (should return 400)")
    params = {
        "city": "sao_paulo",
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/customers/by-city", params=params)
    return print_result(response, 400)

def test_customers_by_city_missing_city():
    """Test /customers/by-city with missing city parameter."""
    print_test("Customers by City - Missing City (should return 400)")
    params = {
        "state": "SP",
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/customers/by-city", params=params)
    return print_result(response, 400)

def test_customers_by_city_invalid_state():
    """Test /customers/by-city with invalid state format."""
    print_test("Customers by City - Invalid State Format (should return 422)")
    params = {
        "state": "SPA",  # 3 letters instead of 2
        "city": "sao_paulo",
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/customers/by-city", params=params)
    return print_result(response, 422)

def test_customers_by_city_limit_out_of_range():
    """Test /customers/by-city with limit out of range."""
    print_test("Customers by City - Limit Out of Range (should return 422)")
    params = {
        "state": "SP",
        "city": "sao_paulo",
        "limit": 100  # Max is 50
    }
    response = requests.get(f"{BASE_URL}/customers/by-city", params=params)
    return print_result(response, 422)

def test_geo_top_states_valid():
    """Test /geo/top-states with valid parameters."""
    print_test("Top States - Valid Request")
    params = {"limit": 10}
    response = requests.get(f"{BASE_URL}/geo/top-states", params=params)
    success = print_result(response, 200)
    if success and response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if len(items) > 0:
            print(f"✅ Found {len(items)} states")
            print(f"   Top state: {items[0].get('state')} with {items[0].get('customer_count')} customers")
    return success

def test_geo_top_states_default():
    """Test /geo/top-states with default limit."""
    print_test("Top States - Default Limit")
    response = requests.get(f"{BASE_URL}/geo/top-states")
    success = print_result(response, 200)
    if success and response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        print(f"✅ Returned {len(items)} states (default limit=10)")
    return success

def test_geo_top_states_limit_out_of_range():
    """Test /geo/top-states with limit out of range."""
    print_test("Top States - Limit Out of Range (should return 422)")
    params = {"limit": 50}  # Max is 27
    response = requests.get(f"{BASE_URL}/geo/top-states", params=params)
    return print_result(response, 422)

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("CUSTOMERS GEO ANALYTICS - TEST SUITE")
    print("="*60)
    print(f"\nTesting against: {BASE_URL}")
    print("Make sure Flask app is running: flask --app app/app.py run\n")

    results = []

    # Health check
    results.append(("Health Check", test_health()))

    # Customers by City tests
    results.append(("Customers by City - Valid", test_customers_by_city_valid()))
    results.append(("Customers by City - Missing State", test_customers_by_city_missing_state()))
    results.append(("Customers by City - Missing City", test_customers_by_city_missing_city()))
    results.append(("Customers by City - Invalid State", test_customers_by_city_invalid_state()))
    results.append(("Customers by City - Limit Out of Range", test_customers_by_city_limit_out_of_range()))

    # Top States tests
    results.append(("Top States - Valid", test_geo_top_states_valid()))
    results.append(("Top States - Default", test_geo_top_states_default()))
    results.append(("Top States - Limit Out of Range", test_geo_top_states_limit_out_of_range()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask app.")
        print("   Make sure Flask is running: flask --app app/app.py run")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)

