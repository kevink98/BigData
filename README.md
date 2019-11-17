# BigData

## Aufgabe
Aufgabe war es, Lieder von einer Spotify-Playlist anhand von ihren Daten zu kategorisieren. Das Ergebniss soll auf einer Website angezeigt werden.

## Übersicht Docker Container
- Hadoop: Datenverwaltung, Datenbanken
- Airflow: Ablaufplan
- MySql: Dantenbank für Webserver
- Php: Webserver

## Ablauf im DAG
 1) Verzeichniss '/user/hadoop/spotify' anlegen, falls nicht vorhanden
 2) Request zu Spotify ausführen:
    - Verzeichniss '/home/airflow/requestData' löschen (falls vorhanden) und wieder anlegen (alte Daten sind weg)
    - Verzeichniss '/home/airflow/requestData/playlist' anlegen
    - Verzeichniss '/home/airflow/requestData/trackdata' anlegen
    - Request an Spotify senden (Lieder von Playlists)
    - Jedes einzelne Lied in einer *.json*-Datei speichern (in '/home/airflow/requestData/playlist/')
    - Für jede Id neuen Request ausführen, bei dem man weitere Lieddaten erhält. Wird jeweils in */trackdata/* gespeichert.
 3) Verzeichniss '/user/hadoop/spotify' leeren (löschen und neu anlegen)
 4) Verzeichniss '/user/hadoop/spotify' anlegen
 5) Verzeichnisse anlegen
    - '/user/hadoop/spotify/rawPlaylist'
    - '/user/hadoop/spotify/rawTrackData'
    - '/user/hadoop/spotify/rawCategories'
    - '/user/hadoop/spotify/final'
 6) *.json*-Dateien von '/home/airflow/requestData/playlist' nach '/user/hadoop/spotify/rawPlaylist/' kopieren
 7) *.json*-Dateien von '/home/airflow/requestData/trackdata' nach '/user/hadoop/spotify/rawTrackData/' kopieren
 8) Anlegen von Tabellen
    - *rawplaylist*
    - *rawtrackdata*
    - *rawcategories*
    - *final*
 9) Daten in *rawcategories* hinzufügen:
    - Metal
    - Classic
    - Rock
    - Vocal
    - Electro
    - Podcast
    - Soul
    - HipHop
 10) Daten in Finaldatenbank schreiben
 11) MySql - Datenbank erstellen
 12) Daten in MySql - Datenbank exportieren
 13) Verzeichniss '/home/airflow/requestData' löschen
    
