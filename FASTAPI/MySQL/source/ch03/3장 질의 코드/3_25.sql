SELECT	Customer.name, book.bookname
FROM	Customer, Orders, Book
WHERE	Customer.custid=Orders.custid AND Orders.bookid=Book.bookid;