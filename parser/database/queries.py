import sqlite3
from typing import List
from parser import tokens


def get_previous_version_failure_weight(cursor: sqlite3.Cursor, name: str, current_version: str) -> int:
    result = cursor.execute(
        """
        SELECT failure_weight
        FROM sequence_diagrams
        WHERE name = '%s' AND version <= '%s'
        ORDER BY version DESC
        LIMIT 1;
        """ % (name, current_version)
    ).fetchone()
    return result[0] if result else 0


def get_count_of_sequence_diagrams(cursor: sqlite3.Cursor) -> int:
    result = cursor.execute(
        """
        SELECT COUNT(*)
        FROM sequence_diagrams;
        """
    ).fetchone()
    return result[0] if result else 0


def check_specific_sequence_diagram_by_name_and_vers(cursor: sqlite3.Cursor, name: str, version: str) -> int:
    result = cursor.execute(
        """
        SELECT 1
        FROM sequence_diagrams
        WHERE name = '%s' AND version = '%s';
        """ % (name, version)
    ).fetchone()
    return result[0] if result else 0


def get_list_of_sequence_diagrams_by_name(cursor: sqlite3.Cursor, name: str) -> List:
    return cursor.execute(
        """
       SELECT * 
        FROM sequence_diagrams
        WHERE name = '%s'
        ORDER BY version DESC;
        """ % name
    ).fetchall()


def get_list_of_sequence_diagrams_ord_by_version_weight(cursor: sqlite3.Cursor) -> List:
    return cursor.execute(
        """
        SELECT * 
        FROM sequence_diagrams
        ORDER BY (path_weight + feature_weight + failure_weight) DESC;
        """
    ).fetchall()


def insert_into_sequence_diagrams(cursor: sqlite3.Cursor, name: str, version: str, path_weight: int, feature_weight: int, failure_weight: int, result: str):
    cursor.execute(
        """
        INSERT INTO sequence_diagrams (id, name, version, path_weight, feature_weight, failure_weight, result)
        VALUES (%s, '%s', '%s', %s, %s, %s, '%s');
        """ % ("NULL", name, version, path_weight, feature_weight, failure_weight, result)
    )


def insert_into_activity_diagrams(cursor: sqlite3.Cursor, name: str, version: str, seq_diag_id: int, path: List[str], result: str):
    cursor.execute(
        """ 
        INSERT INTO activity_diagrams (id, name, version, seq_diag_id, path, result)
        VALUES (%s, '%s', '%s', %d, '%s', '%s');
        """ % ("NULL", name, version, seq_diag_id, str(path).replace("'", ""), result)
    )


def update_sequence_weights_by_name(cursor: sqlite3.Cursor, name: str, path_weight: int, feature_weight: int, failure_weight: int):
    cursor.execute(
        """
        UPDATE sequence_diagrams
        SET path_weight = %s, feature_weight = %s, failure_weight = %s
        WHERE name = '%s';
        """ % (path_weight, feature_weight, failure_weight, name)
    )


def update_failed_sequence_diagram_weight(cursor: sqlite3.Cursor, seq_diag_id: int, failure_weight: int):
    cursor.execute(
        """
        UPDATE sequence_diagrams
        SET failure_weight = sequence_diagrams.failure_weight + %s, result='failed'
         WHERE id = %s;
        """ % (failure_weight, seq_diag_id)
    )


def update_resolved_sequence_diagram_weight(cursor: sqlite3.Cursor, seq_diag_id: int):
    cursor.execute(
        """
        UPDATE sequence_diagrams
        SET failure_weight = 0 WHERE id = %s;
        """ % seq_diag_id
    )


def check_if_seq_has_failed_before(cursor: sqlite3.Cursor, name: str, version: str, seq_diag_id: int, path: List[str]):
    return cursor.execute(
        """
        SELECT 1
        FROM activity_diagrams
        JOIN sequence_diagrams ON sequence_diagrams.id = activity_diagrams.seq_diag_id AND sequence_diagrams.id = %s
        WHERE activity_diagrams.name = '%s' AND activity_diagrams.version = '%s' AND activity_diagrams.path = '%s' AND activity_diagrams.result = '%s'
        """ % (seq_diag_id, name, version, str(path).replace("'", ""), tokens.FAILED)
    ).fetchall()

def update_sequence_diagram_to_passed(cursor: sqlite3.Cursor, seq_diag_id: int):
    cursor.execute(
        """
        UPDATE sequence_diagrams
        SET result = 'passed' WHERE id = %s;
        """ % seq_diag_id
    )