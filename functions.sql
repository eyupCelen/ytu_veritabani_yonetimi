--Seçilen kategoriden ve alt kategorilerinden ürün getirir (recursively)
CREATE OR REPLACE FUNCTION get_categorized_products(ctgry_id category.category_id%TYPE) 
RETURNS TABLE (
    product_id product.product_id%TYPE, 
    product_description product.product_description%TYPE, 
    price product.price%TYPE,
    category_name category.category_name%TYPE
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        P.product_id, 
        P.product_description, 
        P.price,
	C1.category_name
    FROM Product P
    JOIN Category C1 ON C1.category_id = P.category_id
    where P.category_id in (
		WITH RECURSIVE CategoryHierarchy AS (
		    SELECT category_id
		    FROM category
		    WHERE category_id = ctgry_id
		    UNION ALL
		    SELECT C.category_id
		    FROM CategoryHierarchy CH
		    JOIN category C on CH.category_id=C.parent_category_id
		    )
	   	SELECT category_id FROM CategoryHierarchy
	);
END;
$$ LANGUAGE plpgsql;

-- Seçilen kategoriden en az belirtilen puana sahip ürünleri getirir. 
CREATE OR REPLACE FUNCTION get_rated_products(
    min_rating_score real, 
    ctgry_id category.category_id%TYPE
)
RETURNS TABLE (
    product_id product.product_id%TYPE,
    product_description product.product_description%TYPE,
    price product.price%TYPE,
    category_name category.category_name%TYPE
) 
AS $$
BEGIN
    RETURN QUERY
        SELECT 
        R.product_id, 
        R.product_description, 
        R.price,
	R.category_name 
	FROM get_categorized_products(ctgry_id) as R
    WHERE(
            SELECT AVG(review_rating)
            FROM REVIEW
            WHERE REVIEW.product_id = R.product_id
        ) >= min_rating_score;
END;
$$ LANGUAGE plpgsql;

-- Son bir ayın en popüler ürünlerini döndürür
CREATE OR REPLACE FUNCTION get_most_popular_products()
RETURNS TABLE (prod_id INT, total_amount INT) AS $$
DECLARE
    rec RECORD;
    cur CURSOR FOR
        SELECT op.product_id, COUNT(op.product_id) AS total_amount
        FROM Order_Product op
        JOIN Order_ o ON op.order_id = o.order_id
        GROUP BY op.product_id
        HAVING MAX(o.order_time) >= NOW() - INTERVAL '30 days'
        ORDER BY total_amount DESC
        LIMIT 5;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        prod_id := rec.product_id;
        total_amount := rec.total_amount;
        RETURN NEXT; 
    END LOOP;
    CLOSE cur;
END $$ LANGUAGE plpgsql;
