SELECT	name
FROM	Customer
WHERE	custid IN (SELECT custid FROM Orders);