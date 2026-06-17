SELECT	custid, COUNT(*) AS 도서수량, SUM(saleprice) AS 총액
FROM	Orders
GROUP BY	custid;


select * FROM	Orders
order by custid;


SELECT	custid, COUNT(*) AS 도서수량, SUM(saleprice) AS 총액
FROM	Orders
GROUP BY	custid 
ORDER BY  custid; 