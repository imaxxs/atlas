#!/bin/bash

export TZ=EST

function run_integration_test {
    module_directory_to_add="$1"
    if [ -d "${module_directory_to_add}/integration" ]; then
        cd ${module_directory_to_add}
        python -m unittest -f -v integration || exit -1
    fi
}

cwd=`pwd`

for module_directory in $(echo atlas/foundations_*)
do
    run_integration_test "${cwd}/${module_directory}/src"
done
