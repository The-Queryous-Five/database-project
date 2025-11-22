-- complex queries will be collected here

-- average score and count between min_score and max_score
SELECT AVG(review_score) AS avg_score,
       COUNT(*)          AS review_count
FROM order_reviews
WHERE review_score BETWEEN 1 AND 5;
