CREATE EXTERNAL TABLE IF NOT EXISTS rawcategories (
    id STRING, 
    category STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/user/hadoop/spotify/rawCategories';
