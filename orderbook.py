from collections import defaultdict, deque  # a faster insert/pop queue
import math


class OrderBook:
    def __init__(self):
        self.bids = OrderList("B")
        self.asks = OrderList("S")
        self.transcation_log = []  # for checking each transcation
        self.output_log = []

    def parse_order(self, order: str):
        """
        Parse order string in the format of

        SUB LO [Side] [Order ID] [Quantity] [Price]
        Submit a Limit Order with the specified Order ID, Quantity and Price.

        SUB MO [Side] [Order ID] [Quantity]
        Submit a Market Order with the specified Order ID and Quantity.

        CXL [Order ID]
        Cancel the order in the OB with the specified Order ID. If there is no order in the OB with the specified Order ID, this action should do nothing.
        """
        order_command = order.split()
        action = order_command[0]

        if action == 'SUB':
            order_type, side, order_id, quantity = order_command[
                1], order_command[2], order_command[3], int(order_command[4])
            if order_type == 'LO':
                price = int(order_command[5])
                self.process_limit_order(side, order_id, quantity, price)
            elif order_type == 'MO':
                self.process_market_order(side, quantity)
            elif order_type == 'IOC':
                price = int(order_command[5])
                self.process_ioc_order(side, quantity, price)
            elif order_type == "FOK":
                price = int(order_command[5])
                self.process_fok_order(side, quantity, price)

        elif action == 'CXL':
            order_id = order_command[1]
            self.cancel_order(order_id)

        elif action == 'CRP':
            order_id, new_quantity, new_price = order_command[1], int(
                order_command[2]), int(order_command[3])
            self.cancel_replace_order(order_id, new_quantity, new_price)

        elif action == "END":
            self.output_log.append(str(self.bids))
            self.output_log.append(str(self.asks))
            self.get_output()
            return

        self.transcation_log.append(f"{str(self.bids)}, {str(self.asks)}")

    def process_limit_order(self, side, order_id, quantity, price):
        quantity_to_trade = quantity
        if side == 'B':
            if self.asks.num_orders <= 0 or price < self.asks.min_price():
                self.output_log.append(0)
                self.bids.insert_order(
                    side, order_id, quantity_to_trade, price)
                return

            while quantity_to_trade > 0 and self.asks.num_orders > 0 and price >= self.asks.min_price():
                best_ask_price_order = self.asks.get_min_price_order()
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, best_ask_price_order)

            if quantity_to_trade > 0:
                self.bids.insert_order(
                    side, order_id, quantity_to_trade, price)

        elif side == 'S':
            if self.bids.num_orders <= 0 or price > self.bids.max_price():
                self.output_log.append(0)
                self.asks.insert_order(
                    side, order_id, quantity_to_trade, price)
                return

            while quantity_to_trade > 0 and self.bids.num_orders > 0 and price <= self.bids.max_price():
                best_bid_price_order = self.bids.get_max_price_order()
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, best_bid_price_order)

            if quantity_to_trade > 0:
                self.asks.insert_order(
                    side, order_id, quantity_to_trade, price)

        self.store_cost_output(quantity, quantity_to_trade, traded_price)

    def process_market_order(self, side, quantity):
        quantity_to_trade = quantity

        if side == 'B':
            while quantity_to_trade > 0 and self.asks.num_orders > 0:
                priority_order_id = self.asks.order_ids[0]
                priority_order = self.asks.order_map.get(priority_order_id)
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, priority_order)

        elif side == 'S':
            while quantity_to_trade > 0 and self.bids.num_orders > 0:
                priority_order_id = self.bids.order_ids[0]
                priority_order = self.bids.order_map.get(priority_order_id)
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, priority_order)

        self.store_cost_output(quantity, quantity_to_trade, traded_price)

    def process_ioc_order(self, side, quantity, price):
        """
        An IOC Order is similar to a Limit Order, except if the IOC Order is not executed fully,
        the remaining quantity will be cancelled, instead of being added to the OB.
        """
        quantity_to_trade = quantity
        if side == 'B':
            if self.asks.num_orders <= 0 or price < self.asks.min_price():
                self.output_log.append(0)
                return

            while quantity_to_trade > 0 and self.asks.num_orders > 0 and price >= self.asks.min_price():
                best_ask_price_order = self.asks.get_min_price_order()
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, best_ask_price_order)

        elif side == 'S':
            if self.bids.num_orders <= 0 or price > self.bids.max_price():
                self.output_log.append(0)
                return

            while quantity_to_trade > 0 and self.bids.num_orders > 0 and price <= self.bids.max_price():
                best_bid_price_order = self.bids.get_max_price_order()
                quantity_to_trade, traded_price = self.process_order(
                    quantity_to_trade, best_bid_price_order)

        self.store_cost_output(quantity, quantity_to_trade, traded_price)

    def process_fok_order(self, side, quantity, price):
        """
        An FOK Order is similar to a Limit Order, except the FOK Order
        will be executed if and only if it can be executed fully.
        If the FOK Order cannot be executed fully, it will not be executed at
        all - that is, the OB will remain exactly the same.
        """
        traded_value = 0
        quantity_to_trade = quantity
        if side == 'B':
            orders_avaliable = self.asks.get_orders(max_price=price)[::-1]
            orders_qty = self.asks.get_order_quantity(orders_avaliable)
            if orders_qty >= quantity:
                for order in orders_avaliable:
                    if quantity_to_trade > 0:
                        pre_trade_quantity = quantity_to_trade
                        quantity_to_trade, traded_price = self.process_order(
                            quantity_to_trade, order)
                        traded_value += traded_price * \
                            (pre_trade_quantity - quantity_to_trade)
                self.output_log.append(traded_value)

            else:
                self.output_log.append(0)

            return

        elif side == 'S':
            orders_avaliable = self.bids.get_orders(min_price=price)[::-1]
            orders_qty = self.bids.get_order_quantity(orders_avaliable)
            if orders_qty >= quantity:
                for order in orders_avaliable:
                    if quantity_to_trade > 0:
                        pre_trade_quantity = quantity_to_trade
                        quantity_to_trade, traded_price = self.process_order(
                            quantity_to_trade, order)
                        traded_value += traded_price * \
                            (pre_trade_quantity - quantity_to_trade)
                self.output_log.append(traded_value)

            else:
                self.output_log.append(0)

            return

    def process_order(self, quantity_to_trade, target_order_obj):
        """ Processes the order by finding the best price and quantity to trade. """
        traded_price = target_order_obj.price

        if quantity_to_trade > target_order_obj.quantity:
            quantity_to_trade -= target_order_obj.quantity
            target_order_obj.quantity = 0

            if target_order_obj.side == "B":
                self.bids.remove_order(target_order_obj)
            elif target_order_obj.side == "S":
                self.asks.remove_order(target_order_obj)

        elif quantity_to_trade < target_order_obj.quantity:
            target_order_obj.quantity -= quantity_to_trade
            quantity_to_trade = 0

        return quantity_to_trade, traded_price

    def cancel_order(self, order_id):
        if order_id in self.bids.order_map:
            order = self.bids.order_map.get(order_id)
            self.bids.remove_order(order)
        elif order_id in self.asks.order_map:
            order = self.asks.order_map.get(order_id)
            self.asks.remove_order(order)

    def cancel_replace_order(self, order_id, new_quantity, new_price):
        """
        Cancels and replaces a Limit Order in the OB with a new Price and Quantity, keeping the order ID the same.
        Effectively serves as an update to the Quantity and/or Price of a Limit Order within the OB.

        The updated order will be treated as a newly-inserted order, which means it will be given lower priority
        compared to other existing orders of the same Price. The only exception to this rule is when the
        Price remains the same and the Quantity decreases (or also remains the same).
        """
        if order_id in self.bids.order_map:
            self.bids.update_order(order_id, new_quantity, new_price)

        elif order_id in self.asks.order_map:
            self.asks.update_order(order_id, new_quantity, new_price)

    def store_cost_output(self, initial_quantity, final_quantity, price):
        self.output_log.append((initial_quantity - final_quantity) * price)

    def get_output(self) -> str:
        for output in self.output_log:
            print(output)


class OrderList:
    """ Order list stores Order sorted according to price"""

    def __init__(self, side):
        self.price_map = defaultdict(list)  # Dict of price : Order object
        self.prices = PriceList()  # List of prices
        self.order_ids = []  # list of order by priority
        self.order_map = {}  # Dictionary containing order_id : Order object
        self.num_orders = 0  # Contains count of Orders in tree
        self.side = side  # Contains side of the order

    def get_max_price_order(self):
        if self.num_orders > 0:
            print("MAX Price", self.max_price())
            return self.price_map[self.max_price()][0]
        else:
            return None

    def get_min_price_order(self):
        if self.num_orders > 0:
            return self.price_map[self.min_price()][0]
        else:
            return None

    def max_price(self):
        return self.prices.tail.price if self.num_orders > 0 else None

    def min_price(self):
        return self.prices.head.price if self.num_orders > 0 else None

    def order_exists(self, order_id):
        return self.order_map.get(order_id) != None

    def insert_order(self, side, order_id, quantity, price):
        """
        Inserts an order into the order list.
        Adds to the price map, order map, price list of order list.
        """
        order = Order(side, order_id, quantity, price)
        self.price_map[price].append(order)
        self.order_map[order_id] = order
        self.order_ids.append(order_id)
        self.prices.add(price)
        self.num_orders += 1

    def update_order(self, order_id, new_quantity, new_price):

        order = self.order_map.get(order_id)
        if order is None:
            return

        # if price and quantity of new order and existing order is the same, just update the quantitiy of the order without change
        if order.price == new_price and new_quantity <= order.quantity:
            order.quantity = new_quantity
            return
        # else we need to remove the order and add the new order with the same order id
        order_side = order.side
        self.remove_order(order)
        self.insert_order(order_side, order_id, new_quantity, new_price)

    def remove_order(self, order):
        self.remove_order_by_id(order.order_id)
        self.remove_order_by_price(order)

    def remove_order_by_id(self, order_id):
        order = self.order_map.get(order_id)
        self.order_ids.remove(order_id)
        if order != None:
            self.num_orders -= 1
            del self.order_map[order_id]

    def remove_order_by_price(self, order):
        """Removes order from prices list and price map"""
        order_price = order.price
        price_list = self.price_map.get(order_price)
        if price_list != None:
            for i in range(len(price_list)):
                if price_list[i].order_id == order.order_id:
                    del price_list[i]
                    break
            self.prices.remove(order_price)

            if len(price_list) == 0:
                del self.price_map[order_price]
            else:
                self.price_map[order_price] = price_list

    def get_orders(self, min_price=0, max_price=math.inf, side=None):
        """Get order of different prices sorted by order priority"""
        orders = []
        orders_price_id = []
        if side == "B":
            price_list = self.get_price_list(
                min_price, max_price)[::-1]
        else:
            price_list = self.get_price_list(
                min_price, max_price)

        for idx, price in enumerate(price_list):
            # check for duplicates of price in list
            if idx > 0 and price == price_list[idx-1]:
                continue

            orders.extend(
                [order for order in self.price_map[price]])

        # for id in self.order_ids:
        #     if id in orders_price_id:
        #         orders.append(self.order_map[id])

        return orders

    def get_order_quantity(self, order_list):
        """Get the quantity of orders in order list"""
        if len(order_list) == 0:
            return 0
        return sum([order.quantity for order in order_list])

    def get_price_list(self, min_price=0, max_price=math.inf):
        """Get price list between min and max price"""
        price_list = []
        for price in self.prices.get_prices():
            if price >= min_price and price <= max_price:
                price_list.append(price)
        return price_list

    def get_orders_by_id(self):
        """Get order by id priority"""
        orders = []
        for order_id in self.order_ids:
            orders.append(self.order_map[order_id])
        return orders

    def __str__(self) -> str:
        """Returns string representation of the order list sorted by price"""

        order_list = [str(order)
                      for order in self.get_orders(side=self.side)]

        order_str = ''
        for order in order_list:
            order_str += ' ' + order

        return f"{self.side}:{order_str}"


class Order:
    """Order class to store each bid/ask order information."""

    def __init__(self, side, order_id, quantity, price):
        self.side = side
        self.order_id = order_id
        self.quantity = quantity
        self.price = price

    @ property
    def side(self) -> str:
        return self._side

    @ property
    def order_id(self) -> int:
        return self._order_id

    @ property
    def price(self) -> int:
        return self._price

    @ property
    def quantity(self) -> int:
        return self._quantity

    @ property
    def next(self) -> 'Order':
        return self._next

    @ property
    def prev(self) -> 'Order':
        return self._prev

    @ side.setter
    def side(self, side) -> None:
        if side == 'B' or side == 'S':
            self._side = side
        else:
            raise ValueError('Invalid side')

    @ order_id.setter
    def order_id(self, order_id) -> None:
        self._order_id = order_id

    @ price.setter
    def price(self, price) -> None:
        if isinstance(price, int):
            self._price = price
        else:
            raise ValueError('Invalid price')

    @ quantity.setter
    def quantity(self, quantity) -> None:
        if isinstance(quantity, int):
            self._quantity = quantity
        else:
            raise ValueError('Invalid quantity')

    def __str__(self) -> str:
        return f'{self.quantity}@{self.price}#{self.order_id}'


class PriceList:
    """
    Double linked list to store prices and maintain sorted order.
    It allows us to get the min and max price in O(1) time.
    It allows to maintain the sorted insertion order at less or equals to O(N) time.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.num_prices = 0

    def add(self, price):
        """Inserts a price into the sorted price list"""
        node = PriceNode(price)
        if self.head == None:
            self.head = node
            self.tail = self.head
        elif price <= self.head.price:
            self.head.prev = node
            node.next = self.head
            self.head = node
        elif price >= self.tail.price:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        else:
            temp = self.head.next
            current = self.head
            while ((temp is not None) and
                   (temp.price < node.price)):
                temp = temp.next

            temp.prev.next = node
            node.prev = temp.prev
            temp.prev = node
            node.next = temp

        self.num_prices += 1

    def remove(self, price):
        """Remove price from the price list"""
        current = self.head
        while current != None:
            if current.price == price:
                if current.prev == None:
                    self.head = current.next
                else:
                    current.prev.next = current.next
                if current.next == None:
                    self.tail = current.prev
                else:
                    current.next.prev = current.prev
                self.num_prices -= 1
                return
            current = current.next

    def get_prices(self):
        """Returns a list of prices"""
        prices = []
        current = self.head
        while current != None:
            prices.append(current.price)
            current = current.next
        return prices

    def __len__(self):
        return self.num_prices

    def __str__(self) -> str:
        """Returns the string representation of the price list"""
        return str(self.get_prices())


class PriceNode:
    """Node for price in price list"""

    def __init__(self, price):
        self.price = price
        self.next = None
        self.prev = None

    def __str__(self) -> str:
        return f'{self.price}'
