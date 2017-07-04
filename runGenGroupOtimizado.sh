#!/bin/bash
echo "running all instances - genGroupOtimizado"
python genGroupOtimizado.py tkp_instances/U2 cid 200 > genGroupOtimizado_U2_cid_200.txt
python genGroupOtimizado.py tkp_instances/U100 cid 200 > genGroupOtimizado_U100_cid_200.txt
python genGroupOtimizado.py tkp_instances/I5 cid 200 > genGroupOtimizado_I5_cid_200.txt
python genGroupOtimizado.py tkp_instances/I25 cid 200 > genGroupOtimizado_I25_cid_200.txt
python genGroupOtimizado.py tkp_instances/I72 cid 200 > genGroupOtimizado_I72_cid_200.txt
python genGroupOtimizado.py tkp_instances/I90 cid 200 > genGroupOtimizado_I90_cid_200.txt
python genGroupOtimizado.py tkp_instances/I100 cid 200 > genGroupOtimizado_I100_cid_200.txt
python genGroupOtimizado.py tkp_instances/HB5000 cid 200 > genGroupOtimizado_HB5000_cid_200.txt
python genGroupOtimizado.py tkp_instances/HB10000 cid 200 > genGroupOtimizado_HB10000_cid_200.txt
python genGroupOtimizado.py tkp_instances/HB15000 cid 200 > genGroupOtimizado_HB15000_cid_200.txt
