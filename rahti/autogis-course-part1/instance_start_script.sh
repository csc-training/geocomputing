#!/usr/bin/env bash

export JUPYTER_ENABLE_LAB=true

export OPENBLAS_NUM_THREADS=2

cd /home/$NB_USER/work
# git reflog requires a name and email if user is not in passwd
# even if you're only cloning
export GIT_COMMITTER_NAME=anonymous
export GIT_COMMITTER_EMAIL=anon@localhost

# Configure
DIR=/home/jovyan/work/notebooks
if [ -d "$DIR" ]; then
    printf '%s\n' "Removing Lock ($DIR)"
    rm -rf "$DIR"
fi
echo "Cloning git repository now"

git clone https://github.com/geo-python/notebooks.git

# Go to containing folder
#cd /home/jovyan/work/notebooks/notebooks

# backwards compatibility to BOOTSTRAP_* -vars in existing blueprints
#if [ ! -z "$BOOTSTRAP_URL" ]; then
#    AUTODOWNLOAD_URL="$BOOTSTRAP_URL"
#fi
#
#if [ ! -z "$AUTODOWNLOAD_URL" ]; then
#    # custom target filename
#    if [ ! -z "$AUTODOWNLOAD_FILENAME" ]; then
#        echo "Downloading $AUTODOWNLOAD_URL to $AUTODOWNLOAD_FILENAME"
#        wget "$AUTODOWNLOAD_URL" -O "$AUTODOWNLOAD_FILENAME"
#    else
#        echo "Downloading $AUTODOWNLOAD_URL"
#        wget "$AUTODOWNLOAD_URL"
#    fi
#    # execution if desired
#    if [ ! -z "$AUTODOWNLOAD_EXEC" ]; then
#        chmod u+x $AUTODOWNLOAD_EXEC
#        ./$AUTODOWNLOAD_EXEC
#    fi
#    # background execution if desired
#    if [ ! -z "$AUTODOWNLOAD_EXEC_BG" ]; then
#        chmod u+x $AUTODOWNLOAD_EXEC_BG
#        ./$AUTODOWNLOAD_EXEC_BG &
#    fi
#fi


# become the normal startup script
exec /usr/local/bin/start-notebook.sh $* --NotebookApp.token="$INSTANCE_ID"
