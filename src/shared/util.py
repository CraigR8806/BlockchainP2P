import yaml
import jsonpickle
import json
from blockchain.database.document_entry import DocumentEntry
import typing as t

# NEEDS COMMENTING


def read_properties_file(file_name: str) -> t.Dict[str, str]:
    out = None
    with open(file_name, "r") as stream:
        try:
            out = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return out


def jsonify_data(data: any) -> str:
    return jsonpickle.encode(data)


def extract_data(jzon: str) -> t.Any:
    return jsonpickle.decode(jzon)


def documentify_data(data: DocumentEntry) -> t.Dict[t.Any, t.Any]:
    return json.loads(jsonpickle.encode(data))


def dataify_document(document: t.Dict[t.Any, t.Any]) -> DocumentEntry:
    document.pop("_id", None)
    return jsonpickle.decode(json.dumps(document))
