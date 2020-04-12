
# file encoder shortcut
encode(){
	DIR="`pwd`"
	builtin cd $ENCODER_PATH
	if [ -z "$1" ]; then 
		echo "invalid argument"
	else
		python3 encoder.py encode "$DIR/$1"
	fi
	builtin cd $DIR	
}

decode(){
	DIR="`pwd`"
	builtin cd $ENCODER_PATH
	if [ -z "$1" ]; then 
		echo "invalid argument"
	else 
		python3 encoder.py decode "$DIR/$1"
	fi
	builtin cd $DIR
}
