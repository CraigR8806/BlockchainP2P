import yaml
import jsonpickle

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
    
def extract_data(clazz:type, jzon:str):
    return jsonpickle.decode(jzon)