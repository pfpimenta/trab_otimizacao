glpsol --math math_model.mod -d HB5000_GLPK.dat -o HB5000_SOL.sol --log HB5000_LOG.log --tmlim 3600
glpsol --math math_model.mod -d HB10000_GLPK.dat -o HB10000_SOL.sol --log HB10000_LOG.log --tmlim 3600
glpsol --math math_model.mod -d HB15000_GLPK.dat -o HB15000_SOL.sol --log HB15000_LOG.log --tmlim 3600
glpsol --math math_model.mod -d I5_GLPK.dat -o I5_SOL.sol --log I5_LOG.log --tmlim 3600
glpsol --math math_model.mod -d I25_GLPK.dat -o I25_SOL.sol --log I25_LOG.log --tmlim 3600
glpsol --math math_model.mod -d I72_GLPK.dat -o I72_SOL.sol --log I72_LOG.log --tmlim 3600
glpsol --math math_model.mod -d I90_GLPK.dat -o I90_SOL.sol --log I90_LOG.log --tmlim 3600
glpsol --math math_model.mod -d I100_GLPK.dat -o I100_SOL.sol --log I100_LOG.log --tmlim 3600
glpsol --math math_model.mod -d U2_GLPK.dat -o U2_SOL.sol --log U2_LOG.log --tmlim 3600
glpsol --math math_model.mod -d U100_GLPK.dat -o U100_SOL.sol --log U100_LOG.log --tmlim 3600