USE spotify_data;
CREATE TABLE IF NOT EXISTS titledata (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    artists VARCHAR(255),
    category VARCHAR(63)
)
