#!/bin/bash

current_dir_name=$(basename `pwd`)
expected_dir_name="edx-platform"

if [ "$current_dir_name" == "$expected_dir_name" ]; then
    FOLDER_NAME="openedx_edly_discussion"
    cd openedx/features
    git clone https://github.com/edly-io/openedx-nodebb-discussion.git $FOLDER_NAME
    cd ../..
    python openedx/features/$FOLDER_NAME/scripts/integrator.py
    pip install -e .
    ./manage.py lms makemigrations $FOLDER_NAME
    ./manage.py lms migrate $FOLDER_NAME
else
    echo "Please make sure that you are in the correct directorty i.e. ../edx-platform"
fi
