SELECT	Customer.name, saleprice
FROM	Customer LEFT OUTER JOIN Orders
		ON Customer.custid=Orders.custid;