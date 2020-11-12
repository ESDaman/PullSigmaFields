#!/bin/python3
import yaml
import glob

#Written by Evan Daman 
#CAO: 20201112 
#Generates a YAML of field named from Sigma rules. 
#Output used to map field names to individuals' fields for sigmac config. 
#Grouped by Product and Category for field name context. 

FieldList = []
d = {}

for filename in glob.iglob('sigma/rules/**/*.yml', recursive=True):
    print(filename)
    with open(filename, 'r') as f:
        for doc in yaml.safe_load_all(f):
            try:
                product = doc["logsource"]["product"]
                if 'service' in doc["logsource"].keys():
                    service = doc["logsource"]["service"]
                if 'category' in doc["logsource"].keys():
                    service = doc["logsource"]["category"]
                for item in doc["detection"].keys():
                    if 'select' in item:
                        for key in doc['detection'][item]:
                            if ":" in str(key):
                                for subkey in key:
                                    field = subkey
                            else:
                                field = key
                    if 'filter' in item:
                        for key in doc['detection'][item]:
                            if ":" in str(key):
                                for subkey in key.keys():
                                    field = subkey
                            else:
                                field = key
                    if 'exception' in item:
                        for key in doc['detection'][item]:
                            if ":" in str(key):
                                for subkey in key.keys():
                                    field = subkey
                            else:
                                field = key
                if product not in d.keys():
                    d[product] = {}
                if service not in d[product].keys():
                    d[product][service] = []
                d[product][service].append(field)
            except KeyError:
                 pass
result = {}
for key in d.keys():
    if key not in result.keys():
        result[key] = {}
        for key2 in d[key].keys():
            if key2 not in result[key].keys():
                result[key][key2] = []
                for values in d[key][key2]:
                    if values not in result[key][key2]:
                        result[key][key2].append(values)
#print(yaml.dump(result))

with open('FieldList.yml', 'w') as file:
    yaml.dump(result, file)
