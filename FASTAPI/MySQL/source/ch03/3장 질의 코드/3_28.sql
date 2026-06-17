SELECT	bookname
FROM	Book
WHERE	price=(SELECT MAX(price) FROM Book);