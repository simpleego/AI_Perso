UPDATE	book 
SET	publisher = (SELECT	publisher 
				FROM	imported_book 
				WHERE	bookid = '21') 
WHERE	bookid = '14';