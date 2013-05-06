#!/bin/bash
# A small installer script to seperate the linux command
# logic from my python code.
echo $1;
# If the filepath the script is given is a directory,
# then this means the installer needs to use make.
if [ -d $2 ]
then
    cd $2
    ./configure
    make
    if [ -w $3 ]
    then
        echo -e "\n\n Attempting to make install at $2 \n\n"
    else
        echo -e "Attempting to make install at $2 \n\n"
    fi
    sudo make install 2>&1 | tee -a $3
    sleep $4
# If the file path is a real file, then it needs to be
# installed using pip.
elif [ -f $2 ]
then
    sudo pip install $2 --log=$3
    sleep $4
else
    exit 1
fi
