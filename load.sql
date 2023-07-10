CREATE TABLE run (
  id INTEGER PRIMARY KEY,
  dt TIMESTAMP,
  jd TEXT
);

CREATE TABLE bup (
  id INTEGER PRIMARY KEY,
  em VARCHAR,
  nm VARCHAR,
  run_id INTEGER,
  FOREIGN KEY (run_id) REFERENCES run (id)
);

CREATE TABLE sco (
  id INTEGER PRIMARY KEY,
  bup_id INTEGER,
  run_id INTEGER,
  sc INTEGER,
  de INTEGER,
  FOREIGN KEY (bup_id) REFERENCES bup (id),
  FOREIGN KEY (run_id) REFERENCES run (id)
);
