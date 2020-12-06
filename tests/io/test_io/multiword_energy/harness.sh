#!/usr/bin/env bash
export cur_file=$(realpath $0) 
export cur_dir=$(dirname "${cur_file}")
cd "./h_h_mol/UHF_MP2/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/RHF_MP2/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/RHF/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

