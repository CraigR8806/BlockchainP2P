import yaml


def read_properties_file(file_name):
    out=None
    with open(file_name, "r") as stream:
        try:
            out=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return out