import logging
from typing import List

from migrations import mig_01
from parser import calculator
from parser import configurations as conf
from parser import parser
from parser import tokens
from parser.database import db
from parser.database import queries
from parser.dtos import SequenceDiagram


def db_startup():
    with db.get_cursor() as cursor:
        cursor.execute(mig_01.CREATE_SEQUENCE_DIAGRAM_TABLE)
        cursor.execute(mig_01.CREATE_ACTIVITY_DIAGRAM_TABLE)


def log_startup():
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logging.StreamHandler(), logging.FileHandler('logs/service.log')])


def diag_startup():
    """Load and calculate all sequence diagrams."""
    with db.get_cursor() as cursor:
        seq_paths: List[str] = parser.load_diagrams_files(conf.SEQ_DIAGS_DIR)
        for seq_path in seq_paths:
            seq_diag: SequenceDiagram = parser.parse_sequence_diagram(file_path=seq_path)
            seq_diag.path_weight = calculator.calculate_path_weight(seq_diag=seq_diag)
            seq_diag.feature_weight = calculator.calculate_feature_weight(seq_diag=seq_diag)
            seq_diag.failure_weight = queries.get_previous_version_failure_weight(cursor=cursor, name=seq_diag.name, current_version=seq_diag.version)

            if queries.check_specific_sequence_diagram_by_name_and_vers(cursor=cursor, name=seq_diag.name, version=seq_diag.version):
                queries.update_sequence_weights_by_name(
                    cursor=cursor, name=seq_diag.name, path_weight=seq_diag.path_weight, feature_weight=seq_diag.feature_weight, failure_weight=seq_diag.failure_weight
                )

            else:
                queries.insert_into_sequence_diagrams(
                    cursor=cursor, name=seq_diag.name, version=seq_diag.version, path_weight=seq_diag.path_weight, feature_weight=seq_diag.feature_weight, failure_weight=0, result=tokens.NULL
                )
