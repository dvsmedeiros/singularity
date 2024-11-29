from hpccm import Stage
from hpccm.primitives import baseimage, environment, shell
from hpccm.building_blocks import apt_get, mlnx_ofed

# Create a stage object
Stage0 = Stage()

# Specify the base image
Stage0 += baseimage(image='ubuntu:22.04')

# Install essential packages
Stage0 += apt_get(ospackages=['wget', 'make', 'libibverbs-dev', 'libmlx5-1', 'libnuma-dev'])

# Install Python 3.10 (ou uma versão compatível com o openpmix)
Stage0 += apt_get(ospackages=['python3', 'python3-pip', 'python3-venv'])

# Install GCC 12.3 and configure alternatives
# Using version="12" the version installed is 12.3
compiler = gnu(version="12")
Stage0 += compiler

# Install Mellanox OFED driver
Stage0 += mlnx_ofed(version='5.8-3.0.7.0', linux_distro='ubuntu22.04')

Stage0 += openmpi(
    cuda=False, infiniband=True, toolchain=compiler.toolchain, version="5.0.5"
)

# Download and build OSU Micro-Benchmarks
Stage0 += shell(commands=[
    'wget http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.5.tar.gz',
    'tar -xzf osu-micro-benchmarks-7.5.tar.gz',
    'cd osu-micro-benchmarks-7.5',
    './configure CC=mpicc CXX=mpicxx --enable-mpi',
    'make',
    'make install',
    # Ensure executables are moved to /usr/local/bin for easier access
    'cp -r c/mpi/pt2pt/standard/osu_bw /usr/local/bin/'
])

# Configure environment variables
Stage0 += environment(variables={
    'PATH': '/usr/local/bin:$PATH'
})

print(Stage0)