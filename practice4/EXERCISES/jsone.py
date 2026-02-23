# Using data file sample-data.json, create output that resembles the following by parsing the included JSON file.
import json
file_path = 'sample-data.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
print("Interface Status")
print("================================================================================")
print("DN                                                 Description           Speed    MTU")
print("-------------------------------------------------- --------------------  ------  ------")
for item in data["imdata"]:
    att = item["l1PhysIf"]["attributes"]
    dn = att['dn']
    desc = att["pathSDescr"]
    speed = att["speed"]
    mtu = att['mtu']
    print(f"{dn:<50} {desc:<20} {speed:<6} {mtu:<6}")