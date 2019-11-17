CREATE EXTERNAL TABLE IF NOT EXISTS final (
    id STRING, 
    title STRING,
    artist STRING,
    category STRING
) STORED AS ORCFILE LOCATION '/user/hadoop/spotify/final';
