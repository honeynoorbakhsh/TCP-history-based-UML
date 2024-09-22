import os
import xml.etree.ElementTree as ET
from typing import List

from parser import configurations as conf
from parser.dtos import ActivityDiagram, Activity, Flow, SequenceDiagram, Participant, Message
from parser.tokens import STRING, FLOAT, INTEGER

ArgumentTypesMap = {
    STRING: str,
    FLOAT: float,
    INTEGER: int
}


def camel_to_snake(name: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in name.replace(" ", "")]).lstrip("_")


def load_diagrams_files(directory: str) -> List[str]:
    diagrams_paths = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                diagrams_paths.append(file_path)

    return diagrams_paths


def parse_activity_diagram(file_path: str) -> ActivityDiagram:
    tree = ET.parse(file_path)
    root = tree.getroot()

    name = root.attrib.get("name")
    version = root.attrib.get("version")

    activities = []
    for activity_elem in root.find('Activities').findall('Activity'):
        act_id = activity_elem.attrib['id']
        act_name = activity_elem.attrib['name']
        activities.append(Activity(id=act_id, name=act_name))

    flows = []
    for flow_elem in root.find('Flows').findall('Flow'):
        flow = Flow(
            from_activity=flow_elem.attrib['from'],
            to_activity=flow_elem.attrib['to'],
            path_weight=int(flow_elem.attrib['path_weight']),
            feature_weight=int(flow_elem.attrib.get('feature_weight', 0))
        )
        flows.append(flow)

    return ActivityDiagram(name=name, version=version, activities=activities, flows=flows)


def parse_sequence_diagram(file_path: str) -> SequenceDiagram:
    tree = ET.parse(file_path)
    root = tree.getroot()

    name = root.attrib.get("name")
    version = root.attrib.get("version")

    participants = []
    for participant_elem in root.find('Participants').findall('Participant'):
        participant = Participant(
            id=participant_elem.attrib['id'],
            name=participant_elem.attrib['name']
        )
        participants.append(participant)

    messages = []
    for message_elem in root.findall('Message'):
        message = Message(
            from_participant=message_elem.attrib['from'],
            to_participant=message_elem.attrib['to'],
            name=message_elem.attrib['name']
        )
        messages.append(message)

    return SequenceDiagram(name=name, version=version, participants=participants, messages=messages)


def get_activity_diagrams(seq_diag: SequenceDiagram) -> List[ActivityDiagram]:
    activities = []
    for msg in seq_diag.messages:
        act_diag_name: str = camel_to_snake(msg.name)
        activities.append(parse_activity_diagram(conf.ACT_DIAGS_DIR / ("%s.xml" % act_diag_name)))
    return activities
