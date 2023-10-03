
def read_properties_file(file_name):
    separator = "="
    keys = {}
    with open(file_name) as f:

        for line in f:
            if separator in line:
                name, value = line.split(separator, 1)
                keys[name.strip()] = value.strip()
    return keys