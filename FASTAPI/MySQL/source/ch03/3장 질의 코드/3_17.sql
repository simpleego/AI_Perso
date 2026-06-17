SELECT	SUM(saleprice) AS Total,
		AVG(saleprice) AS Average,
		MIN(saleprice) AS Minimum,
		MAX(saleprice) AS Maximum
FROM	Orders;