# BigData

## Aufgabe
Aufgabe war es, Lieder von einer Spotify-Playlist anhand von ihren Daten zu kategorisieren. Das Ergebniss soll auf einer Website angezeigt werden.

## Übersicht Docker Container
- Hadoop: Datenverwaltung, Datenbanken
- Airflow: Ablaufplan
- MySql: Dantenbank für Webserver
- Php: Webserver

## Grober Ablauf
 1) Request zu Spotify: Daten von Playlist 
     - Lieddaten in seperate *.json*-Dateien speichern
 2) Request zu Spotify: Für jedes Lied weitere Lieddaten
     - Lieddaten in seperate *.json*-Dateien speichern
 3) Tabellen in Hadoop anlegen
 4) Daten in Tabellen speichern
 5) Für jedes Lied die Musikkategorie speichern
 6) Finale Daten erzeugen
 7) MySql Tabelle anlegen und Daten aus Finaltabelle importieren
 
## Genauer Ablauf im DAG / Erklärung der einzelnen Tasks
 1) *start*: Verzeichniss '/user/hadoop/spotify' anlegen, falls nicht vorhanden
 2) *request_playlist_operator*: Request zu Spotify ausführen:
    - Verzeichniss '/home/airflow/requestData' löschen (falls vorhanden) und wieder anlegen (alte Daten sind weg)
    - Verzeichniss '/home/airflow/requestData/playlist' anlegen
    - Verzeichniss '/home/airflow/requestData/trackdata' anlegen
    - Request an Spotify senden (Lieder von Playlists)
    - Jedes einzelne Lied in einer *.json*-Datei speichern (in '/home/airflow/requestData/playlist/')
    - Für jede Id neuen Request ausführen, bei dem man weitere Lieddaten erhält. Wird jeweils in */trackdata/* gespeichert.
 3) *empty_spotify*: Verzeichniss '/user/hadoop/spotify' leeren (löschen und neu anlegen)
 4) *create_hdfs_spotify_dir*: Verzeichniss '/user/hadoop/spotify' anlegen
 5) Verzeichnisse anlegen
    - *create_hdfs_spotify_raw_dir*: '/user/hadoop/spotify/rawPlaylist'
    - *create_hdfs_spotify_raw_trackData_dir*: '/user/hadoop/spotify/rawTrackData'
    - *create_hdfs_spotify_raw_categories_dir*: '/user/hadoop/spotify/rawCategories'
    - *create_hdfs_spotify_final_dir*: '/user/hadoop/spotify/final'
 6) *reqDataCopyPlaylist*: *.json*-Dateien von '/home/airflow/requestData/playlist' nach '/user/hadoop/spotify/rawPlaylist/' kopieren
 7) *reqDataCopyTrackData*: *.json*-Dateien von '/home/airflow/requestData/trackdata' nach '/user/hadoop/spotify/rawTrackData/' kopieren
 8) Anlegen von Tabellen
    - *createTableRawPlaylist*: *rawplaylist*
    - *createTableRawTrackData*: *rawtrackdata*
    - *createTableRawCategorie*: *rawcategories*
    - *createTableFinal*: *final*
 9) Daten in *rawcategories* hinzufügen:
    - *insertCategory_metal*: Metal
    - *insertCategory_classic*: Classic
    - *insertCategory_rock*: Rock
    - *insertCategory_vocal*: Vocal
    - *insertCategory_electro*: Electro
    - *insertCategory_podcast*: Podcast
    - *insertCategory_soul*: Soul
    - *insertCategory_hiphop*: HipHop
 10) insertoverwrite_final: Daten in Finaldatenbank schreiben
 11) createTableToMysql: MySql - Datenbank erstellen
 12) exportToMysql: Daten in MySql - Datenbank exportieren
 13) finish_operator: Verzeichniss '/home/airflow/requestData' löschen
 
 ## Projektdateien
  - Dag: [spotify.py](spotify.py)
  - SQL-Hive: [Rawdaten für Plalist](sql/hive/rawplaylist.sql)
  - SQL-Hive: [Rawdaten für Trackdaten](sql/hive/rawtrackdata.sql)
  - SQL-Hive: [Rawdaten für Kategorien](sql/hive/rawcategories.sql)
  - SQL-Hive: [Finaldaten](sql/hive/final.sql)
  - SQL-MySql: [Tieldaten](sql/mysql/titeldata.sql)
  - Webserver: [Startseite](sql/mysql/titeldata.sql)
  - Webserver: Styledateien in Unterordner
 
 ## Probleme
 - Der Authentifizierungscode von Spotify läuft nach einer gewissen Zeit aus. D.h. man muss immer einen neuen beantragen und diesem im Pythonscript aktualisieren. Es gibt auch eine Funktion bei Spotify, wo man automatisch ein Request machen kann und einen neuen erhalten kann. Aus Zeitgründen konnte dieses Feature jedoch nichtmehr implementiert werden.
    
