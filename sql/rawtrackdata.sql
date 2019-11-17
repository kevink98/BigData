CREATE EXTERNAL TABLE IF NOT EXISTS rawtrackdata (
    danceability FLOAT,
    energy FLOAT,
    key FLOAT,
    loudness FLOAT,
    mode FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo STRING,
    id STRING,
    uri STRING,
    track_href STRING,
    anaylsis_url STRING,
    duration_ms STRING,
    time_signature INT    
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
LOCATION '/user/hadoop/spotify/rawTrackData';
