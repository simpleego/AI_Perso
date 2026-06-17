SELECT	*
FROM	Customer, Orders
WHERE	Customer.custid=Orders.custid
ORDER BY	Customer.custid;