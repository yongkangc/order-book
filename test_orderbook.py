# import pytest
import pytest
from orderbook import *
import random
from pprint import pprint


@pytest.fixture
def orders():
    with open('orders2.txt', 'r') as f:
        orders = f.read().splitlines()
        return orders


@pytest.fixture
def limit_orders():
    with open('limit_orders.txt', 'r') as f:
        limit_order = f.read().splitlines()
        return limit_order


@pytest.fixture
def market_orders():
    with open('market_orders.txt', 'r') as f:
        limit_order = f.read().splitlines()
        return limit_order


def test_price_list():
    price = [1, 55, 55, 100, 2, 1, 5000, 1, 0, 55, 3, 23, 46, 0]
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


def test_order_list_price_sort():
    order_list = OrderList("B")
    order_list.insert_order("B", "Ffuj", 200, 13)
    order_list.insert_order("B", "Ff2uj", 20, 13)
    order_list.insert_order("B", "Ff3uj", 30, 3)
    order_list.insert_order("B", "Ff4uj", 40, 20)
    order_list.insert_order("B", "Ff5uj", 50, 1)
    order_list.insert_order("B", "Ff6uj", 60, 1000)
    assert order_list.prices.get_prices() == [1, 3, 13, 13, 20, 1000]


def test_order_list_remove_order_by_id():
    order_list = OrderList("B")
    order_list.insert_order("B", "Ffuj", 200, 13)
    order_list.insert_order("B", "Ff2uj", 20, 13)
    order_list.remove_order_by_id("Ff2uj")
    assert list(order_list.order_map.keys()) == ['Ffuj']


def test_order_list_insert_remove():
    order_list = OrderList("B")
    order_list.insert_order("B", "Ffuj", 200, 13)
    order_list.insert_order("B", "Ff2uj", 20, 13)
    order_list.insert_order("B", "Ff3uj", 30, 3)
    order_list.insert_order("B", "Ff4uj", 40, 20)
    order_list.insert_order("B", "Ff5uj", 50, 1)
    order_list.insert_order("B", "Ff6uj", 60, 1000)
    assert str(
        order_list) == "B : ['50@1#Ff5uj', '30@3#Ff3uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"
    order_list.remove_order(Order("B", "Ff3uj", 30, 3))
    assert str(
        order_list) == "B : ['50@1#Ff5uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"
    order_list.insert_order("B", "D3uj", 30, 3)
    assert str(
        order_list) == "B : ['50@1#Ff5uj', '30@3#D3uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"


def test_parse_order_book(orders):
    ob = OrderBook()
    for order in orders:
        ob.parse_order(order)


def test_order_book_limit_order(limit_orders):
    ob = OrderBook()
    for order in limit_orders:
        ob.parse_order(order)
    assert ob.transcation_log[-1] == "B : ['20@12#I8LO', '300@9#Y5wb', '450@7#IpD8'], S : ['250@14#IpD11']"
    # pprint(ob.transcation_log)


def test_order_book_market_order(market_orders):
    ob = OrderBook()
    for order in market_orders:
        ob.parse_order(order)

    assert ob.transcation_log[-1] == "B : ['350@7#IpD8'], S : ['250@14#IpD9', '290@16#IpD10']"
    # pprint(ob.transcation_log)


if __name__ == '__main__':
    # test_price_list()
    # test_price_list()
    # test_order_list_price_sort()
    # test_order_list_remove_order_by_id()
    # test_order_list_insert_remove()
    test_order_book_limit_order()
