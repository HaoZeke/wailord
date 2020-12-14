#!/bin/bash
#SBATCH -N 1
#SBATCH -J ORCA_CALCULATION
#SBATCH -p normal

#MESSAGE TO THE USER:
#THIS JOB SCRIPT DOES NOT SUPPORT PARALLEL COMPUTATIONS USING ORCA

export job=$SLURM_JOB_NAME
export orcadir="{{cookiecutter.orca_root}}"
export cur_dir=$(realpath $0)

if [ ! -d "/scratch" ]; then
	scratchlocation=/tmp
else
	scratchlocation=/scratch
fi

echo $HOSTNAME

#Create directory in scratch
if [ ! -d $scratchlocation/$USER ]; then
	mkdir -p $scratchlocation/$USER
fi
tdir=$(mktemp -d $scratchlocation/$USER/ORCA__$SLURM_JOBID-XXXX)
chmod +xr $tdir

#check if dir exists
if [ ! -d "$tdir" ]; then
	echo "Scratch dir  does not exist on this node"
	echo "Maybe because scratchlocation $scratchlocation does not exist on node??"
	echo "Or because permissions did not allow creation of folder?"
	echo "Exiting..."
	exit
fi

cp *.inp $tdir/
cp *.xyz $tdir/
cd $tdir

echo "Job execution start: $(date)"
echo "Slurm Job ID is: ${SLURM_JOBID}"
echo "slurm Job name is: ${SLURM_JOB_NAME}"
echo "Scratchdir is: $tdir"

$orcadir/orca orca.inp >orca.out

cp -r $tdir/*.xyz $SLURM_SUBMIT_DIR
cp -r $tdir/*.gbw $SLURM_SUBMIT_DIR
cp -r $tdir/*.out $SLURM_SUBMIT_DIR
cp -r $tdir/*.molden $SLURM_SUBMIT_DIR
cp -r $tdir/*.scfp $SLURM_SUBMIT_DIR
rm -rf $tdir
