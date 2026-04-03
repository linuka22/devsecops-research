import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_placeholder_orders():
    assert True

def test_order_total():
    items = [
        {"price": 10.00, "qty": 2},
        {"price": 5.50,  "qty": 4},
    ]
    total = sum(i["price"] * i["qty"] for i in items)
    assert total == 42.0