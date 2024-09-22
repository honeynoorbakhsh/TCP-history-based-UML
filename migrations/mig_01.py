CREATE_SEQUENCE_DIAGRAM_TABLE = """\
CREATE TABLE IF NOT EXISTS sequence_diagrams (
    id INTEGER PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    version VARCHAR(15) NOT NULL,
    path_weight INTEGER DEFAULT 0,
    feature_weight INTEGER DEFAULT 0,
    failure_weight INTEGER DEFAULT 0,
    result VARCHAR(15) NULL
);
"""
CREATE_ACTIVITY_DIAGRAM_TABLE = """\
CREATE TABLE IF NOT EXISTS activity_diagrams (
    id INTEGER PRIMARY KEY,
    name VARCHAR(25) NULL,
    version VARCHAR(15) NULL,
    seq_diag_id INT NOT NULL,
    path VARCHAR(500) DEFAULT NULL,
    result VARCHAR(15) NULL,
    FOREIGN KEY (seq_diag_id) REFERENCES sequenc_diagrams(id)
);
"""
