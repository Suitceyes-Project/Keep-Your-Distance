#if [[ "$VIRTUAL_ENV" != "cv" ]]
#then
#	echo "Switching to virtual environment"
#	if [[ "$VIRTUAL_ENV" != "" ]]
#	then
#		deactivate
#	fi
#	source ~/.profile
#	workon cv
#fi

echo "Running python script"
cd "$(dirname "$0")"
python police-chase.py headless
