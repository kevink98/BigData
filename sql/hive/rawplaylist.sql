CREATE EXTERNAL TABLE IF NOT EXISTS rawplaylist (
    added_at string,
    added_by struct<external_urls:struct<spotify:string>, href:string, id:string, type:string, uri:string>,
    is_local boolean,
    track struct<id:string, name:string, popularity:int, track_numner:int, type:string, uri:string, artists:array<struct<name:string, href:string, id:string, type:string, uri:string, external_urls:struct<spotify:string>>>>,
    video_thumbnail struct<url:string>
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
LOCATION '/user/hadoop/spotify/rawPlaylist';
