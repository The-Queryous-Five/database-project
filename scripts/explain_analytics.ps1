# Sprint C: EXPLAIN Analytics Queries
# Purpose: Show execution plans for all 4 analytics queries
# Demonstrates index usage and performance optimization

Write-Host "`n╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          Sprint C: EXPLAIN Analysis for Analytics Queries                ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "`n❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "Copy .env.example to .env and configure MySQL credentials." -ForegroundColor Yellow
    exit 1
}

# Python script to run EXPLAIN queries
$pythonScript = @"
import os
import sys
from dotenv import load_dotenv
from app.db.db import get_conn

load_dotenv()

queries = {
    "Revenue by Category": '''
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
        LIMIT 10
    ''',
    
    "Top Sellers": '''
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
        LIMIT 10
    ''',
    
    "Review vs Delivery": '''
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
        HAVING COUNT(DISTINCT r.review_id) >= 50
        ORDER BY avg_review_score DESC, avg_delivery_days ASC
        LIMIT 20
    ''',
    
    "Order Funnel": '''
        SELECT
            order_status,
            COUNT(*) AS order_count,
            ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)), 1) AS avg_delivery_days,
            ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_approved_at)), 1) AS avg_approval_days
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC
    '''
}

try:
    conn = get_conn()
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("EXPLAIN Output for Analytics Queries")
    print("="*80)
    
    for name, query in queries.items():
        print(f"\n{'='*80}")
        print(f"Query: {name}")
        print(f"{'='*80}\n")
        
        explain_query = f"EXPLAIN {query.strip()}"
        cursor.execute(explain_query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Print header
        header = " | ".join(f"{col:15}" for col in columns)
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in cursor.fetchall():
            row_str = " | ".join(f"{str(val)[:15]:15}" if val is not None else " "*15 for val in row)
            print(row_str)
        
        print()
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*80)
    print("✅ EXPLAIN analysis complete!")
    print("="*80)
    print("\nKey columns to check:")
    print("  • 'type': ref/eq_ref (good), ALL (bad - full scan)")
    print("  • 'key': shows which index was used (NULL = no index)")
    print("  • 'rows': number of rows examined (lower is better)")
    print("  • 'Extra': 'Using index' (good), 'Using temporary' (slow)")
    print("\nFor detailed analysis, see: docs/sprint_c/PERFORMANCE.md\n")
    
except Exception as e:
    print(f"\n❌ Error running EXPLAIN: {e}", file=sys.stderr)
    print("\nTroubleshooting:")
    print("  1. Check .env has correct MySQL credentials")
    print("  2. Ensure MySQL service is running")
    print("  3. Verify database 'olist' exists")
    print("  4. Apply indexes: db/ddl_mysql/sprint_c_constraints_indexes.sql\n")
    sys.exit(1)
"@

# Write Python script to temp file
$tempScript = "$env:TEMP\explain_analytics.py"
$pythonScript | Out-File -FilePath $tempScript -Encoding UTF8

# Run Python script
try {
    Write-Host "`nRunning EXPLAIN analysis...`n" -ForegroundColor Yellow
    & ".\venv\Scripts\python.exe" $tempScript
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ EXPLAIN analysis completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ EXPLAIN analysis failed. Check error messages above." -ForegroundColor Red
    }
} finally {
    # Cleanup
    if (Test-Path $tempScript) {
        Remove-Item $tempScript
    }
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
