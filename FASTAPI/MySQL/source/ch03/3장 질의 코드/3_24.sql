SELECT	name, SUM(saleprice)
FROM	Customer, Orders
WHERE	Customer.custid=Orders.custid
GROUP BY	Customer.name
ORDER BY	Customer.name;