#!/usr/bin/env bash
export cur_file=$(realpath $0) 
export cur_dir=$(dirname "${cur_file}")
cd "./h_h_mol/UHF/spin_01/ENERGY/3-21G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-31G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311G8"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311PPG88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311PPG(2d,2p)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311PPG(2df,2pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/UHF/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/3-21G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-31G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311G8"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311PPG88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311PPG(2d,2p)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311PPG(2df,2pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/3-21G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-31G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311G"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311G8"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311G88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311PPG88"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311PPG(2d,2p)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311PPG(2df,2pd)"
qsub './basejob.sh'
cd $cur_dir

cd "./h_h_mol/QCISD(T)/spin_01/ENERGY/6-311PPG(3df,3pd)"
qsub './basejob.sh'
cd $cur_dir

