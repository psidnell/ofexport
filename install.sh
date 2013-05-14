#!/bin/bash

set -e

function intro () {
	clear
	echo INTRODUCTION
	cat LICENSE.MD | grep -v '# Lic'
	echo
	echo What this installer does:
	echo
	echo "    "1. Make sure you\'re running an appropriate version of python.
	echo "    "2. Sets execute permission on `pwd`/bin/ofexport.
	echo "    "3. Prints instructions on how to update your environment to add this command to your \$PATH variable.
	echo
	echo You can re-run this script as many times as you like to get the instructions again.
	echo
	echo More help can be found here:
	echo
	echo 'https://github.com/psidnell/ofexport/blob/master/DOCUMENTATION.md'
	echo
	echo If you\'re happy with this type return to continue.
	echo Otherwise if you\'re in any way unsure type ctrl + C to quit or simply exit the Terminal app.
	read
}

function python_check () {
	PVERSION=`python -V 2>&1 | sed -e 's/.* //'`
	if [[ $PVERSION != 2.7.* ]]; then 
		clear
		echo WARNING: PYTHON PVERSION CHECK FAILURE
		echo
		echo You have python version $PVERSION
		echo
		echo ofexport was tested against python 2.7.2 which comes with Mountain Lion and
		echo while it requires at least some revision of 2.7 it may work with newer versions.
		echo
		echo Type return to continue of ctrl + C to exit or simply exit the Terminal app.
		exit 1
	fi
}


function fix_permissions () {
	chmod +x bin/ofexport
}

function create_example_bashrc () {
	echo > example-bashrc
	echo export OFEXPORT_HOME=\"`pwd`\" >> example-bashrc
	echo export PATH=\$PATH:\"\$OFEXPORT_HOME/bin\" >> example-bashrc
}
function upgrade () {
	clear
	fix_permissions
	create_example_bashrc
	echo UPGRADE INSTRUCTIONS
	echo
	echo It looks like everything is already correctly configured.
	echo
}

function upgrade_and_move () {
	clear
	fix_permissions
	create_example_bashrc
	echo CHANGING INSTALL LOCATION INSTRUCTIONS
	echo
	echo It looks like you\'re installing to a new location since you
	echo already have your OFEXPORT_HOME environment variable set to:
	echo 
	echo OFEXPORT_HOME=\"$OFEXPORT_HOME\"
	echo
	echo If you want to use this new location you will have to edit your \".bashrc\"
	echo file and modify it to contain the following two lines instead:
	cat example-bashrc
	echo
	echo You may re-run this installer once you have modified your environment
	echo and it should detect the correct configuration.
	echo
}

function install () {
	clear
	fix_permissions
	create_example_bashrc
	echo FRESH INSTALL INSTRUCTIONS
	echo
	echo 1. You will need the following two lines in a file called \".bashrc\"
	echo "   "\(if you have one\) in your home folder:
	cat example-bashrc
	echo
	echo "   "You can update/create the file yourself or type:
	echo
	echo 'cat example-bashrc >> ~/.bashrc'
	echo
	echo 2. To refresh your current environment with these changes type:
	echo
	echo '. ~/.bashrc'
	echo
	echo 3. Finally as a test type:
	echo
	echo ofexport -?
	echo
	echo "   "and it should print it\'s help.
	echo
	echo You may re-run this installer once you have modified your environment
	echo and it should detect the correct configuration.
	echo
}

########################################

intro

python_check

if [ "$OFEXPORT_HOME" == "`pwd`" ]; then
	upgrade
elif [ -n "$OFEXPORT_HOME" ]; then
	upgrade_and_move
else
	install
fi
