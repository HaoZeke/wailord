#!/usr/bin/env bash
export cur_file=$(realpath $0) 
export cur_dir=$(dirname "${cur_file}")
cd "./vibf_vpt2_h2o/O1H2_inp/HF/spin_01/VPT2/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./vibf_vpt2_h2o/O1H2_inp/MP2/spin_01/VPT2/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./vibf_vpt2_h2o/O1H2_inp/B3LYP/spin_01/VPT2/6-311G88"
qsub './basejob.sh'
cd $cur_dir

