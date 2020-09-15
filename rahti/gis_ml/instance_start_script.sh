#!/usr/bin/env bash

export JUPYTER_ENABLE_LAB=true
export OPENBLAS_NUM_THREADS=2
export PROJ_LIB=/opt/conda/share/proj
export GDAL_DATA=/opt/conda/share/gdal

# Go to containing folder
cd /home/jovyan/work/

git clone https://github.com/csc-training/geocomputing.git
cd geocomputing/machineLearning/2020/excercises

# backwards compatibility to BOOTSTRAP_* -vars in existing blueprints
if [ ! -z "$BOOTSTRAP_URL" ]; then
    AUTODOWNLOAD_URL="$BOOTSTRAP_URL"
fi

if [ ! -z "$AUTODOWNLOAD_URL" ]; then
    # custom target filename
    if [ ! -z "$AUTODOWNLOAD_FILENAME" ]; then
        echo "Downloading $AUTODOWNLOAD_URL to $AUTODOWNLOAD_FILENAME"
        wget -N "$AUTODOWNLOAD_URL" -O "$AUTODOWNLOAD_FILENAME"
    else
        echo "Downloading $AUTODOWNLOAD_URL"
        wget -N "$AUTODOWNLOAD_URL"
    fi
    # execution if desired
    if [ ! -z "$AUTODOWNLOAD_EXEC" ]; then
        chmod u+x $AUTODOWNLOAD_EXEC
        ./$AUTODOWNLOAD_EXEC
    fi
    # background execution if desired
    if [ ! -z "$AUTODOWNLOAD_EXEC_BG" ]; then
        chmod u+x $AUTODOWNLOAD_EXEC_BG
        ./$AUTODOWNLOAD_EXEC_BG &
    fi
fi


# become the normal startup script
exec /usr/local/bin/start-notebook.sh $* --NotebookApp.token="$INSTANCE_ID"
