from typing import List

from parser import boot, tokens
from parser import calculator
from parser import configurations as conf
from parser import executor
from parser import parser
from parser.database import db
from parser.database import queries
from parser.dtos import SequenceDiagram, ActivityDiagram
from scenarios.scn_stuffs import SCNException

if __name__ == '__main__':
    boot.log_startup()
    boot.db_startup()
    boot.diag_startup()

    with db.get_cursor() as cursor_1:
        for result in queries.get_list_of_sequence_diagrams_ord_by_version_weight(cursor=cursor_1):
            file_name: str = parser.camel_to_snake(result[1])
            seq_diag: SequenceDiagram = parser.parse_sequence_diagram(conf.SEQ_DIAGS_DIR / ("%s.xml" % file_name))
            act_diags: List[ActivityDiagram] = parser.get_activity_diagrams(seq_diag=seq_diag)
            for act_diag in act_diags:
                path_ids: List[str] = []
                try:
                    for activity in act_diag.activities:
                        path_ids.append(activity.id)
                        if scn := executor.find_scenario(parser.camel_to_snake(activity.name)):
                            try:
                                executor.exec_scenario(scn)

                            except SCNException as e:
                                with db.get_cursor() as cursor_2:
                                    queries.insert_into_activity_diagrams(cursor=cursor_2, name=act_diag.name, version=act_diag.version, seq_diag_id=result[0], path=path_ids, result=tokens.FAILED)
                                raise

                        with db.get_cursor() as cursor_3:
                            if queries.check_if_seq_has_failed_before(cursor=cursor_3, name=act_diag.name, version=act_diag.version, seq_diag_id=result[0], path=path_ids):
                                queries.update_resolved_sequence_diagram_weight(cursor=cursor_3, seq_diag_id=result[0])

                    with db.get_cursor() as cursor_4:
                        queries.update_sequence_diagram_to_passed(cursor=cursor_4, seq_diag_id=result[0])

                except SCNException as e:
                    failure_hash: int = calculator.calculate_failure_hash(diag_name=act_diag.name, diag_version=act_diag.version, path=path_ids)
                    failure_weight: int = calculator.calculate_failure_weight(failure_hash=failure_hash)

                    with db.get_cursor() as cursor_4:
                        queries.update_failed_sequence_diagram_weight(cursor=cursor_4, seq_diag_id=result[0], failure_weight=failure_weight)
                    break

