hdfs dfs -put prakashbalraj/books_scrape_data.csv /tmp/books/

drop table if exists books_product_details;

create external table books_product_details(
name	string,
url_img	string,
rating	string,
price	double,
stock string,
product_category string,
category_url string
)
row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
stored as textfile
location '/tmp/books/';
