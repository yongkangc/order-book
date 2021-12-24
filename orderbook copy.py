from collections import deque  # a faster insert/pop queue
from sortedcontainers import SortedDict


class OrderBook:
    def __init__(self):
        self.trades = deque()
        self.bids = OrderList()
        self.asks = OrderList()

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
        action, order_type, side, order_id, quantity, price = order_command
        print(action, order_type, side, order_id, quantity, price)
        if action == 'SUB':
            pass

        elif action == 'CXL':  # cancel order
            pass

    def insert_order(self, order: Order):
        pass

    def cancel_order(self, side, order_id):
        if side == 'bid':
            if self.bids.order_exists(order_id):
                self.bids.remove_order_by_id(order_id)
        elif side == 'ask':
            if self.asks.order_exists(order_id):
                self.asks.remove_order_by_id(order_id)

    def submit_order(self):
        pass


class OrderList:
    """
    Order list stores sorted Order batch according to price 
    """

    def __init__(self):
        self.price_map = []  # Tuple containing list of price,OrderBatch object
        self.prices = []  # List of prices in the orderbook
        self.order_map = {}  # Dictionary containing order_id : Order object
        self.volume = 0  # Contains total quantity from all Orders in tree
        self.num_orders = 0  # Contains count of Orders in tree
        self.depth = 0

    def remove_order_by_id(self, order_id):
        self.num_orders -= 1
        order = self.order_map[order_id]
        self.volume -= order.quantity
        order.order_list.remove_order(order)
        if len(order.order_list) == 0:
            self.remove_price(order.price)
        del self.order_map[order_id]


class OrderBatch:
    """
    OrderBatch uses doubly linkedlist to store orders at the same price. 
    This allow us to fuffil multiple orders at the same price.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.order_qty = 0

    def append_order(self, order):
        """
        Append a new order to the batch.
        """
        if self.size == 0:
            order.next = None
            order.prev = None
            self._head = order
            self._tail = order

        else:
            order.prev = self.tail
            order.next = None
            self.tail.next = order
            self.tail = order

        self.size += 1
        self.order_qty += order.qty

    def remove_order(self, order):
        """
        Remove order from the batch
        """
        if self.size == 0:  # return if the batch is empty
            return

        if order.prev is None:  # if the order is the head
            self.head = order.next
            self.head.prev = None

        elif order.next is None:  # if the order is the tail
            self.tail = order.prev
            self.tail.next = None

        else:  # if the order is in the middle
            order.prev.next = order.next
            order.next.prev = order.prev

        self.size -= 1
        self.order_qty -= order.qty

    def update_order(self, order):
        """
        Update the order in the batch. When the order is not finished processing, move it to the back.
        """
        pass


class Order:
    """
    Order class to store each bid/ask order information. 
    """

    def __init__(self, side, order_id, price, quantity):
        self.side = side
        self.order_id = int(order_id)
        self.price = int(price)
        self.quantity = int(quantity)

        # Using doubly linked list to rearrange the orders easier according to price
        self.next = None
        self.prev = None

    @property
    def side(self) -> str:
        return self._side

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def price(self) -> int:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def next(self) -> 'Order':
        return self._next

    @property
    def prev(self) -> 'Order':
        return self._prev

    @side.setter
    def side(self, side) -> None:
        if side == 'B' or side == 'S':
            self._side = side
        else:
            raise ValueError('Invalid side')

    @order_id.setter
    def order_id(self, order_id) -> None:
        if isinstance(order_id, int):
            self._order_id = order_id
        else:
            raise ValueError('Invalid order id')

    @price.setter
    def price(self, price) -> None:
        if isinstance(price, int):
            self._price = price
        else:
            raise ValueError('Invalid price')

    @quantity.setter
    def quantity(self, quantity) -> None:
        if isinstance(quantity, int):
            self._quantity = quantity
        else:
            raise ValueError('Invalid quantity')

    def __str__(self) -> str:
        return f'{self.side}@{self.price}#{self.order_id}'
