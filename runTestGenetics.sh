#!/bin/bash
echo " --- running all versions once for U2 amd once for I100 ---"
python gena.py tkp_instances/U2 seedMoreira 200
python genaSemRep.py tkp_instances/U2 seedMoreira 200
python genaSemRep2.py tkp_instances/U2 seedMoreira 200
python genaGroup.py tkp_instances/U2 seedMoreira 200
python gena.py tkp_instances/I100 seedMoreira 200
python genaSemRep.py tkp_instances/I100 seedMoreira 200
python genaSemRep2.py tkp_instances/I100 seedMoreira 200
python genaGroup.py tkp_instances/I100 seedMoreira 200
