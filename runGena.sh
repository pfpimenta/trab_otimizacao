#!/bin/bash
echo "running all instances - genaSemRep2"
python gena.py tkp_instances/U2 seedMoreira 200 > gena_U2_seedMoreira_200.txt
python gena.py tkp_instances/U100 seedMoreira 200 > gena_U100_seedMoreira_200.txt
python gena.py tkp_instances/I5 seedMoreira 200 > gena_I5_seedMoreira_200.txt
python gena.py tkp_instances/I25 seedMoreira 200 > gena_I25_seedMoreira_200.txt
python gena.py tkp_instances/I72 seedMoreira 200 > gena_I72_seedMoreira_200.txt
python gena.py tkp_instances/I90 seedMoreira 200 > gena_I90_seedMoreira_200.txt
python gena.py tkp_instances/I100 seedMoreira 200 > gena_I100_seedMoreira_200.txt
python gena.py tkp_instances/HB5000 seedMoreira 200 > gena_HB5000_seedMoreira_200.txt
python gena.py tkp_instances/HB10000 seedMoreira 200 > gena_HB10000_seedMoreira_200.txt
python gena.py tkp_instances/HB15000 seedMoreira 200 > gena_HB15000_seedMoreira_200.txt
