# Alpha lab Matching Engine

Approach to the problem:

Price Node -> Price List (Doubly Linked List) -> Order -> Order List -> Order Book

Practices used :

- Test driven development is used as correctness is very important for the implementation of order book.

### Testing

Test Everything : ` pytest -vv | tee test.log`

`pytest -k'test_order_book' -vv -s | tee test.log`

`pytest -k'test_order_book_market' -vv -s | tee test.log`

### References

https://web.archive.org/web/20110410160306/http://howtohft.wordpress.com:80/2011/02/15/how-to-build-a-fast-limit-order-book

https://www.youtube.com/watch?v=Iaiw5iGjXbw&ab_channel=RichardHolowczak
