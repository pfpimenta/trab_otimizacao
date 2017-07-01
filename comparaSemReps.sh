#!/bin/bash
echo "comparando SemRep com SemRep2"
python genaSemRep.py tkp_instances/I5 seedMoreira 200 > genaSemRep_I5_seedMoreira_200.txt
python genaSemRep2.py tkp_instances/I5 seedMoreira 200 > genaSemRep2_I5_seedMoreira_200.txt
echo " seedMoreira I5 foi"
python genaSemRep.py tkp_instances/I5 cid 200 > genaSemRep_I5_cid_200.txt
python genaSemRep2.py tkp_instances/I5 cid 200 > genaSemRep2_I5_cid_200.txt
echo " cid I5 foi"
python genaSemRep.py tkp_instances/U2 seedMoreira 150 > genaSemRep_U2_seedMoreira_150.txt
python genaSemRep2.py tkp_instances/U2 seedMoreira 150 > genaSemRep2_U2_seedMoreira_150.txt
echo " seedMoreira U2 foi"
python genaSemRep.py tkp_instances/U2 cid 150 > genaSemRep_U2_cid_150.txt
python genaSemRep2.py tkp_instances/U2 cid 150 > genaSemRep2_U2_cid_150.txt
echo " cid U2 foi"
