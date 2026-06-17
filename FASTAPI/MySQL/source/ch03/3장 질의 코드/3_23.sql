SELECT	name, saleprice
FROM	Customer, Orders
WHERE	Customer.custid=Orders.custid;