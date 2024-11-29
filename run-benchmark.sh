#!/bin/bash
#PBS -N osu_benchmark
#PBS -q paralela
#PBS -l nodes=2:ppn=128
#PBS -l walltime=02:00:00
#PBS -m abe
#PBS -j oe
#PBS -o osu_benchmark_output.log

module load singularity
module load openmpi

# Caminho da imagem do contêiner
CONTAINER_IMAGE=~/singularity/osu_benchmark.sif

# Comando para rodar o benchmark osu_bw entre os nós
mpirun --map-by ppn:1:node -np 2 singularity exec $CONTAINER_IMAGE /usr/local/bin/osu_bw