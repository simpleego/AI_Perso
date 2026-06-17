SELECT	name, address
FROM	Customer cs
WHERE	EXISTS (SELECT *
		        FROM	   Orders od
				WHERE   cs.custid=od.custid);