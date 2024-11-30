
# Singularity VM Setup and OSU Benchmark Execution

This document outlines the steps to set up a Singularity environment using a Multipass VM, install necessary dependencies, and execute OSU micro-benchmarks.

## 1. Launch and Access the VM
Run the following commands to create and access the Multipass VM:
```bash
multipass launch -n singularity-vm -d 40G --mount ~/:/Users/dvsmedeiros/dev/projects/repositories/singularity
multipass shell singularity-vm
```

## 2. Install Dependencies
Update the repositories and install required packages:
```bash
sudo apt-get update
sudo apt-get install -y \
   autoconf \
   automake \
   cryptsetup \
   fuse \
   fuse2fs \
   git \
   libfuse-dev \
   libglib2.0-dev \
   libseccomp-dev \
   libtool \
   pkg-config \
   runc \
   squashfs-tools \
   squashfs-tools-ng \
   uidmap \
   wget \
   zlib1g-dev
```

## 3. Install Go
Install the Go programming language:
```bash
export VERSION=1.22.6 OS=linux ARCH=amd64
wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz
sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz
rm go$VERSION.$OS-$ARCH.tar.gz
```
Add Go to the PATH:
```bash
echo 'export GOPATH=${HOME}/go' >> ~/.bashrc
echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc
source ~/.bashrc
```

## 4. Install Singularity
Download and install Singularity:
```bash
export VERSION=4.2.0
wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-ce-${VERSION}.tar.gz
tar -xzf singularity-ce-${VERSION}.tar.gz
cd singularity-ce-${VERSION}

git clone --recurse-submodules https://github.com/sylabs/singularity.git
cd singularity
git checkout --recurse-submodules v4.2.0

sudo apt install make
./mconfig
make -C ./builddir
sudo make -C ./builddir install
```

## 5. Install HPC Container Maker (HPCCM)
Install HPCCM via pipx:
```bash
sudo apt install pipx
pipx ensurepath
pipx install hpccm
```

## 6. Transfer Recipe and Build the Singularity Image
Transfer the `recipe.py` file to the VM:
```bash
multipass transfer ./recipe.py singularity-vm:/home/ubuntu
```
Generate the Singularity definition file:
```bash
/home/ubuntu/.local/share/pipx/venvs/hpccm/bin/hpccm --recipe recipe.py --format singularity > Singularity.def
```
Build the Singularity image:
```bash
sudo singularity build osu_benchmark.sif Singularity.def
```
Transfer the Singularity image back to your local machine:
```bash
multipass transfer singularity-vm:/home/ubuntu/osu_benchmark.sif ./
```

## 7. Upload Image to CENAPAD
Access the CENAPAD cluster and upload the image:
```bash
ssh -p 31459 d290281@cenapad.unicamp.br
scp -P 31459 -r ~/dev/projects/repositories/singularity d290281@cenapad.unicamp.br:~/homelovelace/singularity
```

## 8. Execute OSU Micro-Benchmarks
Run the OSU bandwidth benchmark:
```bash
mpirun --map-by ppr:1:node -np 2 singularity exec $CONTAINER_IMAGE /usr/local/bin/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw
```
Replace `$CONTAINER_IMAGE` with the path to your Singularity image.