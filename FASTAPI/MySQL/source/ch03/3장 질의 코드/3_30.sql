SELECT	name
FROM	Customer
WHERE	custid IN(SELECT	custid
				FROM		Orders
				WHERE		bookid IN(SELECT	bookid
									FROM		Book
									WHERE	publisher='대한미디어'));