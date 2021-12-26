# Alpha lab Matchin Engine Challenge Part 1

Approach to the problem:

Binary tree is used as datastructure for holding the list of orders for bid and ask. This will be called OrderTree.
The reason why binary tree is used is because it allows us to detect a match faster.

With this structure you can easily implement these key operations with good performance:

Add – O(log M) for the first order at a limit, O(1) for all others
Cancel – O(1)
Execute – O(1)
GetVolumeAtLimit – O(1)
GetBestBid/Offer – O(1)

Each order list is implemented

Practices used :

- Test driven development is used as correctness is very important for the implementation of order book.

### Testing

Test Everything : ` pytest -vv | tee test.log`

`pytest -k'test_order_book' -vv -s | tee test.log`

`pytest -k'test_order_book_market' -vv -s | tee test.log`

### References

https://web.archive.org/web/20110410160306/http://howtohft.wordpress.com:80/2011/02/15/how-to-build-a-fast-limit-order-book

https://www.youtube.com/watch?v=Iaiw5iGjXbw&ab_channel=RichardHolowczak
