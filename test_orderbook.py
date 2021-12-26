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
    expected_output = ['0', '0', '0', '0', '0', '2100',
                       '2850', 'B: 80@14#Y5wb 100@13#YuFU 150@11#Yy7P', 'S:']
    assert ob.output_log == expected_output

# def test_order_book_2(orders2):
#     ob = OrderBook()
#     for order in orders2:
#         ob.parse_order(order)
#     pprint(ob.transcation_log)
#     assert ob.transcation_log[-1] == "B : ['200@11#0Gxb', '170@11#9zS1', '400@11#2va9'], S : ['320@15#uH6w']"


if __name__ == '__main__':
    # test_price_list()
    # test_price_list()
    # test_order_list_price_sort()
    # test_order_list_remove_order_by_id()
    # test_order_list_insert_remove()
    test_order_book_limit_order()
