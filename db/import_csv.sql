CREATE TABLE IF NOT EXISTS parsed_data(
    book_title VARCHAR(200),
    book_genre VARCHAR(100),
    book_img VARCHAR(200),
    book_rating VARCHAR(15),
    book_description TEXT,
    book_upc varchar(20) PRIMARY KEY,
    book_price_excl_tax DOUBLE PRECISION,
    book_price_incl_tax DOUBLE PRECISION,
    book_tax DOUBLE PRECISION,
    book_available INTEGER,
    book_number_of_reviews INTEGER
);

COPY parsed_data(book_title, book_genre, book_img, book_rating, book_description, book_upc, book_price_excl_tax, book_price_incl_tax, book_tax, book_available, book_number_of_reviews)
FROM '/docker-entrypoint-initdb.d/parsedData.csv'
DELIMITER ';'
CSV HEADER;