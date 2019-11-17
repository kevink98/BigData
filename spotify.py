
"""
Title: Spotify 
Author: Kevin Knoeller
Description: -
"""

import requests, json, os, shutil

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.hdfs_operations import HdfsPutFileOperator, HdfsGetFileOperator, HdfsMkdirFileOperator
from airflow.operators.filesystem_operations import CreateDirectoryOperator
from airflow.operators.filesystem_operations import ClearDirectoryOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.hive_to_mysql import HiveToMySqlTransfer

args = {
'owner': 'airflow'
}

dag = DAG('spotify', default_args=args, description='Songs from Spotify',
schedule_interval='56 18 * * *',
start_date=datetime(2019, 10, 16), catchup=False, max_active_runs=1)

spotify_token = 'BQBmWsP0MfeeSsKg5nkZaQoHxMrSaxO8DF1JSRAIqGjV2sjDwxOysUleCNj3isnvoTIx_eT0cUT8oxU1Kv_O5FSKI1L9MvWGjYK0A5fSjFK3xCuOhu5FLMCgiZ4-fSALeSo6o6bvBqunhZXqZ9txkNBZwg'
url = "https://api.spotify.com/v1/playlists/37i9dQZF1DWX7rdRjOECPW?fields=fields%3Dtracks.items(track(name%2Chref%2Calbum(name%2Chref)))"
url_trackinfo = "https://api.spotify.com/v1/audio-features/{id}"
headers = {'Accept': 'application/json', 'Content-type': 'application/json', 'Authorization': 'Bearer ' + spotify_token}

jsonPath_requestPlaylist = '/home/airflow/requestData/playlist/{i}.json'
jsonPath_requestTrackdata = '/home/airflow/requestData/trackdata/{i}.json'

dummy_operator2 = DummyOperator(
	task_id='copy_tracks', 
	dag=dag)
dummy_operator3 = DummyOperator(
	task_id='copy_trackdata', 
	dag=dag)
dummy_operator4 = DummyOperator(
	task_id='create_table', 
	dag=dag)
dummy_operator5 = DummyOperator(
	task_id='insert_category', 
	dag=dag)
        
def request_playlist():
    #Delete request folder
    p = '/home/airflow/requestData'
    if os.path.exists(p):
        shutil.rmtree(p)
    
    os.mkdir(p)

    #Create folder for playlist data
    p = '/home/airflow/requestData/playlist'
    os.mkdir(p)

    #Create folder for trackdata data
    p = '/home/airflow/requestData/trackdata'
    os.mkdir(p)

    print('Start playlist request')
    response = requests.get(url=url, headers=headers)

    if "\"status\": 401, \"message\": \"The access token expired\"" in json.dumps(response.json())  : 
        raise ValueError('401: The access token expired')
    else:        
        i = 0
        for item in response.json()['tracks']['items']:
            with open(jsonPath_requestPlaylist.replace('{i}', str(i), 1), 'w') as outfile:
                json.dump(item, outfile)   
            request_trackdata(item['track']['id'], i)
            i += 1
            
    print('Request playlist finish')

def request_trackdata(id, i):
    print('Start trackdata request')
    response = requests.get(url=url_trackinfo.replace("{id}", id, 1), headers=headers)    
    if "\"status\": 401, \"message\": \"The access token expired\"" in json.dumps(response.json()): 
        raise ValueError('401: The access token expired')        
    else:
        with open(jsonPath_requestTrackdata.replace('{i}', str(i), 1), 'w') as outfile:
            json.dump(response.json(), outfile)     

    print('Request finish')

def finish():
    p = '/home/airflow/requestData'
    if os.path.exists(p):
        shutil.rmtree(p)


########################################################### S Q L - S T A T E M E N T S  ################################################################
hiveSql_createTableRawPlaylist='''
CREATE EXTERNAL TABLE IF NOT EXISTS rawplaylist (
    added_at string,
    added_by struct<external_urls:struct<spotify:string>, href:string, id:string, type:string, uri:string>,
    is_local boolean,
    track struct<id:string, name:string, popularity:int, track_numner:int, type:string, uri:string, artists:array<struct<name:string, href:string, id:string, type:string, uri:string, external_urls:struct<spotify:string>>>>,
    video_thumbnail struct<url:string>
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
LOCATION '/user/hadoop/spotify/rawPlaylist';
'''

hiveSql_createTableRawTrackData='''
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
'''

hiveSQL_createTableRawCategories='''
CREATE EXTERNAL TABLE IF NOT EXISTS rawcategories (
    id STRING, 
    category STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/user/hadoop/spotify/rawCategories';
'''

hiveSQL_createTableFinal='''
CREATE EXTERNAL TABLE IF NOT EXISTS final (
    id STRING, 
    title STRING,
    artist STRING,
    category STRING
) STORED AS ORCFILE LOCATION '/user/hadoop/spotify/final';
'''

hiveSQL_insertCategory_metal='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Metal"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.energy > 0.8
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_classic='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Classic"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.tempo < 0.5 and d.speechiness > 0.3
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_rock='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Rock"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.loudness > -10
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_vocal='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Vocal"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.speechiness > 0.7
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_electro='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Elektro"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.speechiness < 0.33
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_podcast='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Podcast"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.instrumentalness > 0.8 and d.speechiness > 0.7
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_soul='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "Soul"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.valence < 0.7 and d.valence > 0.3
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertCategory_hiphop='''
INSERT INTO rawcategories
SELECT
    t.track.id,
    "HipHop"
FROM
    rawplaylist t
    LEFT JOIN rawtrackdata d ON (t.track.id = d.id)
WHERE
   d.tempo > 0.150 and d.speechiness > 0.33 and d.speechiness < 0.66
   AND NOT EXISTS (SELECT 1 FROM rawcategories rc WHERE rc.id = t.track.id);
'''

hiveSQL_insertoverwrite_final='''
INSERT OVERWRITE TABLE final
SELECT
    t.track.id STRING, 
    t.track.name STRING,
    concat_ws(',',t.track.artists.name),
    c.category STRING
FROM
    rawplaylist t LEFT JOIN rawcategories c ON (t.track.id = c.id)
'''

hiveSQL_create_mysql='''
USE spotify_data;
CREATE TABLE IF NOT EXISTS titledata (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    artists VARCHAR(255),
    category VARCHAR(63)
)
'''

########################################################### E M P T D A T A B A S E ################################################################

empty_spotify = BashOperator(
    task_id='empty_rawPlaylist',
    bash_command='hadoop fs -rm -r /user/hadoop/spotify',
    dag=dag,
)

########################################################### M A K E D I R ################################################################
start = HdfsMkdirFileOperator(
    task_id='start',
    directory='/user/hadoop/spotify',
    hdfs_conn_id='hdfs',
    dag=dag,
)
create_hdfs_spotify_dir = HdfsMkdirFileOperator(
    task_id='create_hdfs_spotify_dir',
    directory='/user/hadoop/spotify',
    hdfs_conn_id='hdfs',
    dag=dag,
)
create_hdfs_spotify_raw_dir = HdfsMkdirFileOperator(
    task_id='create_hdfs_spotify_raw_dir',
    directory='/user/hadoop/spotify/rawPlaylist',
    hdfs_conn_id='hdfs',
    dag=dag,
)
create_hdfs_spotify_raw_trackData_dir = HdfsMkdirFileOperator(
    task_id='create_hdfs_spotify_raw_trackData_dir',
    directory='/user/hadoop/spotify/rawTrackData',
    hdfs_conn_id='hdfs',
    dag=dag,
)
create_hdfs_spotify_raw_categories_dir = HdfsMkdirFileOperator(
    task_id='create_hdfs_spotify_raw_categories_dir',
    directory='/user/hadoop/spotify/rawCategories',
    hdfs_conn_id='hdfs',
    dag=dag,
)
create_hdfs_spotify_final_dir = HdfsMkdirFileOperator(
    task_id='create_hdfs_spotify_raw_categories_dir',
    directory='/user/hadoop/spotify/final',
    hdfs_conn_id='hdfs',
    dag=dag,
)

########################################################### S Q L ################################################################
createTableRawPlaylist = HiveOperator(
    task_id='create_table_raw_playlist',
    hql=hiveSql_createTableRawPlaylist,
    hive_cli_conn_id='beeline',
    dag=dag)

createTableRawTrackData = HiveOperator(
    task_id='createTableRawTrackData',
    hql=hiveSql_createTableRawTrackData,
    hive_cli_conn_id='beeline',
    dag=dag)

createTableRawCategorie = HiveOperator(
    task_id='createTableRawCategorie',
    hql=hiveSQL_createTableRawCategories,
    hive_cli_conn_id='beeline',
    dag=dag)

createTableFinal = HiveOperator(
    task_id='createTableFinal',
    hql=hiveSQL_createTableFinal,
    hive_cli_conn_id='beeline',
    dag=dag)    
    
insertCategory_metal = HiveOperator(
    task_id='insertCategory_metal',
    hql=hiveSQL_insertCategory_metal,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_classic = HiveOperator(
    task_id='insertCategory_classic',
    hql=hiveSQL_insertCategory_classic,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_rock = HiveOperator(
    task_id='insertCategory_rock',
    hql=hiveSQL_insertCategory_rock,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_vocal = HiveOperator(
    task_id='insertCategory_vocal',
    hql=hiveSQL_insertCategory_vocal,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_electro = HiveOperator(
    task_id='insertCategory_electro',
    hql=hiveSQL_insertCategory_electro,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_podcast = HiveOperator(
    task_id='insertCategory_podcast',
    hql=hiveSQL_insertCategory_podcast,
    hive_cli_conn_id='beeline',
    dag=dag)
    
insertCategory_soul = HiveOperator(
    task_id='insertCategory_soul',
    hql=hiveSQL_insertCategory_soul,
    hive_cli_conn_id='beeline',
    dag=dag)

insertCategory_hiphop = HiveOperator(
    task_id='insertCategory_hiphop',
    hql=hiveSQL_insertCategory_hiphop,
    hive_cli_conn_id='beeline',
    dag=dag)

insertoverwrite_final = HiveOperator(
    task_id='insertoverwrite_final',
    hql=hiveSQL_insertoverwrite_final,
    hive_cli_conn_id='beeline',
    dag=dag)

createTableToMysql = MySqlOperator(
    mysql_conn_id='mysql',
    task_id='createTableToMysql',
    sql=hiveSQL_create_mysql,
    database='spotify_data',
    dag=dag)

exportToMysql = HiveToMySqlTransfer(
    task_id='exportToMysql',
    sql="SELECT * FROM final",
    mysql_preoperator ='DELETE FROM spotify_data.titledata',
    mysql_table ='spotify_data.titledata',
    mysql_conn_id ='mysql',
    hiveserver2_conn_id = 'beeline',
    dag=dag)

########################################################### C O P Y ################################################################
i = 0
if os.path.exists('/home/airflow/requestData/playlist'):
    for filename in os.listdir('/home/airflow/requestData/playlist'):
        if filename.endswith(".json"):
            reqDataCopyPlaylist = HdfsPutFileOperator(
                task_id='requestdata_copy_playlist' + str(i),
                local_file='/home/airflow/requestData/playlist/' + filename,
                remote_file='/user/hadoop/spotify/rawPlaylist/' + filename,
                hdfs_conn_id='hdfs',
                dag=dag,
            ) 
            i += 1
            dummy_operator2 >> reqDataCopyPlaylist
            reqDataCopyPlaylist >> dummy_operator3   
else:
    dummy_operator2 >> dummy_operator3 

i = 0
if os.path.exists('/home/airflow/requestData/trackdata'):
    for filename in os.listdir('/home/airflow/requestData/trackdata'):
        if filename.endswith(".json"):
            reqDataCopyTrackData = HdfsPutFileOperator(
                task_id='reqDataCopyTrackData' + str(i),
                local_file='/home/airflow/requestData/trackdata/' + filename,
                remote_file='/user/hadoop/spotify/rawTrackData/' + filename,
                hdfs_conn_id='hdfs',
                dag=dag,
            ) 
            i += 1
            dummy_operator3 >> reqDataCopyTrackData
            reqDataCopyTrackData >> dummy_operator4   
else:
    dummy_operator3 >> dummy_operator4    


########################################################### T R E E ################################################################
request_playlist_operator = PythonOperator(task_id='Request_playlist', python_callable=request_playlist, dag=dag)
finish_operator = PythonOperator(task_id='finish', python_callable=finish, dag=dag)

start >> request_playlist_operator >> empty_spotify >> create_hdfs_spotify_dir

create_hdfs_spotify_dir >> create_hdfs_spotify_raw_dir >> dummy_operator2
create_hdfs_spotify_dir >> create_hdfs_spotify_raw_trackData_dir >> dummy_operator2
create_hdfs_spotify_dir >> create_hdfs_spotify_raw_categories_dir >> dummy_operator2
create_hdfs_spotify_dir >> create_hdfs_spotify_final_dir >> dummy_operator2

dummy_operator4 >> createTableRawPlaylist >> dummy_operator5
dummy_operator4 >> createTableRawTrackData >> dummy_operator5
dummy_operator4 >> createTableRawCategorie >> dummy_operator5
dummy_operator4 >> createTableFinal >> dummy_operator5

dummy_operator5 >> insertCategory_metal >> insertCategory_classic >> insertCategory_rock >> insertCategory_vocal >> insertCategory_electro >> insertCategory_podcast>> insertCategory_soul >> insertCategory_hiphop 
insertCategory_hiphop >> insertoverwrite_final >> createTableToMysql >> exportToMysql >> finish_operator


