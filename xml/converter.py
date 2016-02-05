#!/bin/python3

import json
import xmltodict

def xml_to_dict(filename):
  with open(filename,'r') as f:
    s = f.read()
    my_dict = json.dumps(xmltodict.parse(s))
    with open('polar30.py','w') as o:
      o.write(my_dict)    


xml_to_dict('polar30.xml')

