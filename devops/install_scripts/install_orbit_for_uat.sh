#!/bin/bash

mkdir orbit_install && \
cd orbit_install && \
conda create -n orbit_env python=3.6 --yes && \
source ~/anaconda3/etc/profile.d/conda.sh && \
conda activate orbit_env && \
aws s3 cp --quiet $1 ./orbit_installer.sh && \
echo 'Downloaded successfully' && \
chmod +x orbit_installer.sh && \
yes | ./orbit_installer.sh
orbit-server start > /dev/null 2>&1 &
mkdir -p test && \
echo import foundations >> test/main.py && \
chmod +x /home/ubuntu/wait_for_successful_job_submission.sh && \
bash /home/ubuntu/wait_for_successful_job_submission.sh 50