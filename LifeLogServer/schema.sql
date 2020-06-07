DROP TABLE IF EXISTS weight;
CREATE TABLE weight (
  id TEXT,
  datetime INTEGER,
  weight REAL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS auth_token;
CREATE TABLE auth_token (
  token TEXT UNIQUE,
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS cache;
CREATE TABLE cache (
  uuid TEXT,
  token TEXT,
  request_time INTEGER,
  response BLOB,
  PRIMARY KEY (uuid)
)
