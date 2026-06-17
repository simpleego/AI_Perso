SELECT	b1.bookname
FROM	Book b1
WHERE	b1.price > (SELECT 	avg(b2.price)
					FROM	Book b2
					WHERE	b2.publisher=b1.publisher);