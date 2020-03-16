# Atlas Multinode On Premise Installtion

The following document outlines how to setup and deploy a multi-node compute system that runs Atlas, including Keycloak backed authentication, to an on premises cluster.

At a high level, the goals are as follows:

* Setup a master node for orchestrating job execution

* Setup a worker node for executing jobs

* Setup a common storage element for the machines to talk to each other

* Setup user accounts

* Have a user interact with the system

This setup is ideal for teams of Machine Learning Engineers who want to share resources and run Deep Learning jobs an on-premise compute cluster. 

## Prerequisites

* A networked file system to use as a shared configuration location for all nodes

* 1 node to be used as a master machine

* 1 or more nodes to be used as worker instances

## Setup the master node

### Installing and setting up Atlas

1. SSH into the machine to be used as the master instance

2. Download the installer file (atlas_installer.py) on to your machine from our [Github Releases](https://github.com/dessa-oss/atlas/releases) page.

3. Create a conda environment to gurantee no dependency conflicts (e.g. `conda create -y -n atlas python=3.6.8`)

4. Activate the conda environment (e.g. `conda activate atlas`)

5. Run the installer: `python atlas_installer.py`

6. Create a directory that will be the same path on each node (e.g. `sudo mkdir -p /atlas_work_dir`)

7. Edit the permissions on this directory to be accessible by your user (e.g. `sudo chmod pippin:pippin /atlas_work_dir`)

!!! tip
    Running `python atlas_installer.py --help` will show all available installer flags.

!!! note "Importace of a consistant path"
    The path created in step 6 must be the exact same path created on all machines. This is because the configuration file will be shared between all
    machines in the cluster, meaning that whatever is specified in the configuration file in the next section must exist on all machines. **We recommed
    using the name of the path given above for easy debugging.**


### Update the configuration files

By default, the configuration files created by running the Atlas installer are setup for a local configuration. To get everything to communicate
with the required remote locations, we have to update the configuration files manually. Specifically, this includes pointing to the remote Redis
instance and giving the paths to the necessary directories.

**~/.foundations/config/local_docker_scheduler/database.config.yaml**

* Replace the 4 instances of `atlas-ce-tracker` with the Master nodes IP

* Replace the 4 instances of `6379` with `5556`

**~/.foundations/config/local_docker_scheduler/tracker_client_plugins.yaml**

* Replace `atlas-ce-tracker` with the Master nodes IP

* Replace `6379` with `5556`

**~/.foundations/config/local_docker_scheduler/worker_config/execution/default.config.yaml**

* Replace `atlas-ce-tracker` with the Master nodes IP

* Replace `6379` with `5556`

**~/.foundations/config/local_docker_scheduler/worker_config/submission/scheduler.config.yaml**

* Replace `atlas-ce-local-scheduler` with the Master nodes IP

* Replace the *value* in the field `working_dir_root` to be the path to the directory created in *step 6* (e.g. `atlas_work_dir`)

**~/.foundations/config/submission/scheduler.config.yaml**

* Change `working_dir_root` to be `job_store_dir_root`

* Add `working_dir_root: <DIRECTORY_FROM_STEP_6>` to the bottom of the file, making sure to fill in `<DIRECTORY_FROM_STEP_6>`


### Setup the networked file system

The shared file system makes 2 things very easy for us: sharing the configuration files across all machines and the movement of jobs within the system. With
the following steps, we make sure that the master node is hooked up properly and that the configuration files that we updated are in a location to be shared
with all other machines that connect to this file system.

1. Backup the Foundations home directory (e.g. `cp -r ~/.foundations ~/.BACK_foundations`)

2. Mount the networked storage to the Foundations home directory (e.g. `sudo mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/foundations_home ~/.foundations`)

3. Copy the contents of the backed-up directory into the newly mounted directory (e.g. `cp -r ~/.BACK_foundations/* ~/.foundations`)


### Starting Atlas Server

Due to the fact that Atlas is setup to run locally out of the box, we must give it some extra information to kick things into a distributed mindset.

1. Set environment variables
  
  * `export HOST_ADDRESS=http://<CURRENT_NODES_IP>:5000/`
  
  * `export REDIS_ADDRESS=<MASTER_NODES_IP>`
  
  * `export NUM_WORKERS=0`, which will mean this master node will not be used for computing jobs. Default is 1 if not provided.
  
2. Run `atlas-server start`

!!! note "Enabling authentication"
    If you want to run Atlas with authentication, you can run `atlas-server start -p`. More information can be found [here](https://docs.atlas.dessa.com/en/latest/atlas-modes/authentication/). **Authentication is only needed on the master node.**

!!! note "Distributed scheduler"
    To achieve a multi-node scheduler, a lookup table if maintained within the Redis provided by `REDIS_ADDRESS`. This lookup table allows for discovery
    of what scheduler node (via `HOST_ADDRESS`) is running which job at a specific time. This means that when a request comes into the master node for
    information on a particular job, the information provided through these environment variables allow the request to be proxied to the correct scheduler
    instance.


## Setup worker node

The steps below are very similar to all previous steps on this page, they simply have to be repeated on each node that you would like to add
to the cluster.

1. SSH into the machine to be used as a worker instance

2. Download the installer file (atlas_installer.py) on to your machine from our [Github Releases](https://github.com/dessa-oss/atlas/releases) page.

3. Create a conda environment to gurantee no dependency conflicts (e.g. `conda create -y -n atlas python=3.6.8`)

4. Activate the conda environment (e.g. `conda activate atlas`)

5. Run the installer: `python atlas_installer.py`

6. Create a directory that will be the same path on each node (e.g. `sudo mkdir -p /atlas_work_dir`)

7. Edit the permissions on this directory to be accessible by your user (e.g. `sudo chmod pippin:pippin /atlas_work_dir`)

8. Mount the networked storage to the Foundations home directory (e.g. `sudo mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/foundations_home ~/.foundations`)

9. Set environment variables

    * `export HOST_ADDRESS=http://<CURRENT_NODES_IP>:5000/`
    
    * `export REDIS_ADDRESS=<MASTER_NODES_IP>`
    
    * `export NUM_WORKERS=1`
    
10. Run `atlas-server start`

!!! danger "Workers"
    The `NUM_WORKERS` environment variable dictates how many jobs can be run concurrently on this machine. Feel free to adjust
    how you see fit but be aware that Atlas does not manage RAM or CPU resources for you.
    
!!! note "GPUs"
    To use GPUs, you can use `atlas-server start -g` as documented [here](https://docs.atlas.dessa.com/en/latest/atlas-modes/gpu/).
    
## Setup users client

Once both the master and worker(s) instances are setup to handle job submission, we can now set up users to be able to submit jobs. The user will need to install both Atlas, and have the proper submission configuration file.

The Atlas dashboard can be accessed via: `<master_external_ip>:5555`.

The following steps outline the configurations for a user to have on their client machine in order to submit jobs:

1. (As an admin) Create a user account in the Keycloak admin console (`https://<master_node_external_ip>:8443`) by going to "Atlas" realm > Users > Add User

2. (As an admin) Give the user the provided installer file (atlas_installer.py) from [here](https://github.com/dessa-oss/atlas/releases)

3. (As an admin) Give the user the configuration file on the master machine under `~/.foundations/config/submission/scheduler.config.yaml`

4. (As a user) Download the provided atlas_installer.py file onto the machine

5. (As a user) Create a conda environment (e.g. `conda create -y -n atlas python=3.6.8`)

6. (As a user) Activate the conda environment (e.g. `conda activate atlas`)

7. (As a user) Run `python atlas_installer.py -di` to install the Foundations Python SDK

8. (As a user) Rename the given configuration file from `scheduler.config.yaml` to `remote.config.yaml`

9. (As a user) Update the configuration file by changing the `scheduler_url` field from `http://127.0.0.1:5000` to `http://<master_external_ip>:5558`

10. (As a user) Put the configuration file in `~/.foundations/config/submission/remote.config.yaml`


## Test job submission

1. Activate the conda environment that you ran the atlas_installer.py in (e.g. `conda activate atlas`)

2. Run `foundations init <project_name>` to create a simple project with Foundations' scaffolding

3. Change directory into the newly created project directory

4. Run `foundations submit remote . main.py`, where `remote` is the first part of the config we just added

5. Head to the Atlas Dashboard (`http://<master_external_ip>:5555`), login, and checkout your job!
