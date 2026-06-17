SELECT	name
FROM	Customer
WHERE 	address LIKE '대한민국%'
UNION  
SELECT	name
FROM	Customer
WHERE	custid IN (SELECT custid FROM Orders);


SELECT	name
FROM	Customer
WHERE address LIKE '대한민국%'
UNION ALL
SELECT	name
FROM	Customer
WHERE	custid IN (SELECT custid FROM Orders);