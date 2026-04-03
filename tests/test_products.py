import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_placeholder_products():
    assert True

def test_price_calculation():
    price = 29.99
    quantity = 3
    total = price * quantity
    assert round(total, 2) == 89.97