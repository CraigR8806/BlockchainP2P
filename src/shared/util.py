import yaml
import jsonpickle
from bson.json_util import dumps
import bson.json_util as u
from blockchain.database.document_entry import DocumentEntry

def read_properties_file(file_name):
    out=None
    with open(file_name, "r") as stream:
        try:
            out=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return out


def jsonify_data(data:any):
    return jsonpickle.encode(data)
    
def extract_data(jzon:str):
    return jsonpickle.decode(jzon)

def documentify_data(data:DocumentEntry):
     return data.as_document()

