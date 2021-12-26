# import pytest
import pytest
from orderbook import *
import random
from pprint import pprint


@pytest.fixture
def orders():
    with open('orders.txt', 'r') as f:
        orders = f.read().splitlines()
        return orders


@pytest.fixture
def orders2():
    with open('orders2.txt', 'r') as f:
        orders2 = f.read().splitlines()
        return orders2


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


@pytest.fixture
def ioc_orders():
    with open('ioc_orders.txt', 'r') as f:
        ioc_order = f.read().splitlines()
        return ioc_order


@pytest.fixture
def fok_orders():
    with open('fok_orders.txt', 'r') as f:
        fok_orders = f.read().splitlines()
        return fok_orders


@pytest.fixture
def crp_orders():
    with open('crp_orders.txt', 'r') as f:
        crp_orders = f.read().splitlines()
        return crp_orders


def test_order_book_1(orders):
    ob = OrderBook()
    for order in orders:
        ob.parse_order(order)
    print(ob.output_log)
    expected_output = [0, 0, 0, 0, 0, 2100, 2850,
                       'B: 80@14#Y5wb 100@13#YuFU 150@11#Yy7P', 'S:']
    assert ob.output_log == expected_output


def test_order_book_2(orders2):
    ob = OrderBook()
    for order in orders2:
        ob.parse_order(order)
        print(ob.output_log)

    pprint(ob.transcation_log[4:])
    print(ob.output_log[4:])
    expected_output = [0, 0, 0, 0, 1800, 4900, 0, 2350, 0, 0,
                       'B: 200@11#OGxb 170@11#9zS1 480@11#2va9 ', 'S: 320@15#11B6w']
    # assert ob.output_log == expected_output


def test_order_book_fok_order(fok_orders):
    ob = OrderBook()
    for order in fok_orders:
        ob.parse_order(order)

    pprint(ob.transcation_log[-1])
    pprint(ob.transcation_log[-2])
    print(ob.output_log)
