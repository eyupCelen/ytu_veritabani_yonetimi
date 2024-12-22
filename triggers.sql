CREATE OR REPLACE FUNCTION notify_price_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price <> OLD.price THEN
        RAISE NOTICE 'Price of product % has changed from % to %',
            OLD.product_id, OLD.price, NEW.price;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_price_change
AFTER UPDATE OF price
ON Product
FOR EACH ROW
EXECUTE FUNCTION notify_price_change();

-----------------

CREATE OR REPLACE FUNCTION notify_order_cancellation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Order with ID % has been canceled.', OLD.order_id;
    RETURN OLD; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_cancellation_notice
AFTER DELETE ON Order_
FOR EACH ROW
EXECUTE FUNCTION notify_order_cancellation();
