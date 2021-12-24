# import pytest
import pytest
from orderbook import *
import random


@pytest.fixture
def orders():
    with open('orders.txt', 'r') as f:
        orders = f.read().splitlines()
        return orders


def test_split_order():
    with open('orders.txt', 'r') as f:
        orders = f.read().splitlines()

    return orders


def test_price_list():
    price = [55, 55, 100, 2, 1, 5000, 1, 0, 55, 3, 23, 46, 0]
    price_list = PriceList()
    for i in price:
        price_list.add(i)

    price_sorted = sorted(price)
    print(price_list.get_prices())
    assert price_list.get_prices() == price_sorted

    price.remove(0)
    price_sorted = sorted(price)
    price_list.remove(0)
    assert price_list.get_prices() == price_sorted


def test_order():
    order = Order("B", "Ffuj", 200, 13)
    assert order.side == "B"
    assert order.order_id == "Ffuj"
    assert order.quantity == 200
    assert order.price == 13


def test_order_list_str():
    order_list = OrderList("B")
    order_list.insert_order("B", "Ffuj", 200, 13)
    assert str(order_list) == "B : ['200@13#Ffuj']"
    order_list.insert_order("B", "Ff2uj", 20, 13)
    assert str(order_list) == "B : ['200@13#Ffuj', '20@13#Ff2uj']"
    order_list.insert_order("B", "Ff3uj", 30, 3)
    order_list.insert_order("B", "Ff4uj", 40, 20)
    order_list.insert_order("B", "Ff5uj", 50, 1)
    order_list.insert_order("B", "Ff6uj", 60, 1000)
    assert str(
        order_list) == "B : ['200@13#Ffuj', '20@13#Ff2uj', '30@3#Ff3uj', '40@20#Ff4uj', '50@1#Ff5uj', '60@1000#Ff6uj']"
    order_list.remove_order_by_id("Ff2uj")
    assert str(
        order_list) == "B : ['200@13#Ffuj', '30@3#Ff3uj', '40@20#Ff4uj', '50@1#Ff5uj', '60@1000#Ff6uj']"
    order_list.remove_order(Order("B", "Ff3uj", 30, 3))
    assert str(
        order_list) == "B : ['200@13#Ffuj', '40@20#Ff4uj', '50@1#Ff5uj', '60@1000#Ff6uj']"
    order_list.insert_order("B", "D3uj", 30, 3)
    assert str(
        order_list) == "B : ['200@13#Ffuj', '40@20#Ff4uj', '50@1#Ff5uj', '60@1000#Ff6uj', '30@3#D3uj']"
    # assert order_list.__str__() == "B Ffuj 200 13\nB Ff2uj 20 13\nB Ff3uj 30 3\nB Ff4uj 40 20\nB Ff5uj 50 1\nB Ff6uj 60 1000\n"


# def test_remove_object_from_list():
#     class Test:
#         def __init__(self, name):
#             self.name = name

#         def __str__(self):
#             return self.name
#     test_order = [Test("test1"), Test("test2"), Test("test3")]
#     test_order.remove(Test("test2"))
#     assert test_order == [Test("test1"), Test("test3")]


if __name__ == '__main__':
    # test_price_list()
    test_order_list_str()

# test_split_order()
# ob = OrderBook()
# orders = test_split_order()
# for order in orders:
#     ob.parse_order(order)
# print(ob.transcation_log)
