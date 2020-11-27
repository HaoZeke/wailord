#!/usr/bin/env bash
export cur_file=$(realpath $0) 
export cur_dir=$(dirname "${cur_file}")
cd "./ch2_singlet/RHF/spin_01/OPT/3-21G"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-31G"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311G"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311G8"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311PPG88"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311PPG(2d,2p)"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311PPG(2df,2pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./ch2_singlet/RHF/spin_01/OPT/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

