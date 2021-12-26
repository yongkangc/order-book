# # import pytest
# import pytest
# from orderbook import *
# import random
# from pprint import pprint


# @pytest.fixture
# def orders():
#     with open('orders.txt', 'r') as f:
#         orders = f.read().splitlines()
#         return orders


# @pytest.fixture
# def orders2():
#     with open('orders2.txt', 'r') as f:
#         orders2 = f.read().splitlines()
#         return orders2


# @pytest.fixture
# def limit_orders():
#     with open('limit_orders.txt', 'r') as f:
#         limit_order = f.read().splitlines()
#         return limit_order


# @pytest.fixture
# def market_orders():
#     with open('market_orders.txt', 'r') as f:
#         limit_order = f.read().splitlines()
#         return limit_order


# @pytest.fixture
# def ioc_orders():
#     with open('ioc_orders.txt', 'r') as f:
#         ioc_order = f.read().splitlines()
#         return ioc_order


# @pytest.fixture
# def fok_orders():
#     with open('fok_orders.txt', 'r') as f:
#         fok_orders = f.read().splitlines()
#         return fok_orders


# @pytest.fixture
# def crp_orders():
#     with open('crp_orders.txt', 'r') as f:
#         crp_orders = f.read().splitlines()
#         return crp_orders


# def test_price_list():
#     price = [1, 55, 55, 100, 2, 1, 5000, 1, 0, 55, 3, 23, 46, 0]
#     price_list = PriceList()
#     for i in price:
#         price_list.add(i)

#     price_sorted = sorted(price)
#     print(price_list.get_prices())
#     assert price_list.get_prices() == price_sorted

#     price.remove(0)
#     price_sorted = sorted(price)
#     price_list.remove(0)
#     assert price_list.get_prices() == price_sorted


# def test_order():
#     order = Order("B", "Ffuj", 200, 13)
#     assert order.side == "B"
#     assert order.order_id == "Ffuj"
#     assert order.quantity == 200
#     assert order.price == 13


# def test_order_list_price_sort():
#     order_list = OrderList("B")
#     order_list.insert_order("B", "Ffuj", 200, 13)
#     order_list.insert_order("B", "Ff2uj", 20, 13)
#     order_list.insert_order("B", "Ff3uj", 30, 3)
#     order_list.insert_order("B", "Ff4uj", 40, 20)
#     order_list.insert_order("B", "Ff5uj", 50, 1)
#     order_list.insert_order("B", "Ff6uj", 60, 1000)
#     assert order_list.prices.get_prices() == [1, 3, 13, 13, 20, 1000]


# def test_order_list_remove_order_by_id():
#     order_list = OrderList("B")
#     order_list.insert_order("B", "Ffuj", 200, 13)
#     order_list.insert_order("B", "Ff2uj", 20, 13)
#     order_list.remove_order_by_id("Ff2uj")
#     assert list(order_list.order_map.keys()) == ['Ffuj']


# # def test_order_list_insert_remove():
# #     order_list = OrderList("B")
# #     order_list.insert_order("B", "Ffuj", 200, 13)
# #     order_list.insert_order("B", "Ff2uj", 20, 13)
# #     order_list.insert_order("B", "Ff3uj", 30, 3)
# #     order_list.insert_order("B", "Ff4uj", 40, 20)
# #     order_list.insert_order("B", "Ff5uj", 50, 1)
# #     order_list.insert_order("B", "Ff6uj", 60, 1000)
# #     assert str(
# #         order_list) == "B : ['50@1#Ff5uj', '30@3#Ff3uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"
# #     order_list.remove_order(Order("B", "Ff3uj", 30, 3))
# #     assert str(
# #         order_list) == "B : ['50@1#Ff5uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"
# #     order_list.insert_order("B", "D3uj", 30, 3)
# #     assert str(
# #         order_list) == "B : ['50@1#Ff5uj', '30@3#D3uj', '200@13#Ffuj', '20@13#Ff2uj', '40@20#Ff4uj', '60@1000#Ff6uj']"


# def test_order_book_1(orders):
#     ob = OrderBook()
#     for order in orders:
#         ob.parse_order(order)
#     assert ob.transcation_log[-1] == "B : ['80@14#Y5wb', '100@13#YuFU', '150@11#Yy7P'], S : []"


# def test_order_book_limit_order(limit_orders):
#     ob = OrderBook()
#     for order in limit_orders:
#         ob.parse_order(order)
#     assert ob.transcation_log[-1] == "B : ['20@12#I8LO', '300@9#Y5wb', '450@7#IpD8'], S : ['250@14#IpD11']"


# def test_order_book_market_order(market_orders):
#     ob = OrderBook()
#     for order in market_orders:
#         ob.parse_order(order)

#     assert ob.transcation_log[-1] == "B : ['350@7#IpD8'], S : ['250@14#IpD9', '290@16#IpD10']"
#     # pprint(ob.transcation_log)


# def test_order_book_ioc_order(ioc_orders):
#     ob = OrderBook()
#     for order in ioc_orders:
#         ob.parse_order(order)
#     assert ob.transcation_log[-1] == "B : ['450@7#IpD8'], S : ['250@10#IpD9', '290@12#IpD10']"


# def test_order_book_fok_order(fok_orders):
#     ob = OrderBook()
#     for order in fok_orders:
#         ob.parse_order(order)

#     assert ob.transcation_log[-2] == "B : ['100@9#Y5wb', '450@7#IpD8'], S : ['250@10#IpD9', '290@12#IpD10']"
#     assert ob.transcation_log[-1] == "B : ['100@9#Y5wb', '450@7#IpD8'], S : ['250@10#IpD9', '290@12#IpD10']"


# def test_order_book_crp_orders(crp_orders):
#     ob = OrderBook()
#     for order in crp_orders:
#         ob.parse_order(order)
#     assert ob.transcation_log[-2] == "B : ['300@9#Y5wb', '450@7#IpD8'], S : ['250@14#IpD9', '190@14#IpD10', '200@14#IpD11', '130@16#IpD1X1']"
#     assert ob.transcation_log[-1] == "B : ['300@9#Y5wb', '450@7#IpD8'], S : ['250@14#IpD9', '200@14#IpD11', '500@14#IpD10', '130@16#IpD1X1']"


# def test_order_book_2(orders2):
#     ob = OrderBook()
#     for order in orders2:
#         ob.parse_order(order)
#     pprint(ob.transcation_log)
#     assert ob.transcation_log[-1] == "B : ['200@11#0Gxb', '170@11#9zS1', '400@11#2va9'], S : ['320@15#uH6w']"


# if __name__ == '__main__':
#     # test_price_list()
#     # test_price_list()
#     # test_order_list_price_sort()
#     # test_order_list_remove_order_by_id()
#     # test_order_list_insert_remove()
#     test_order_book_limit_order()
