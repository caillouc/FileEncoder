
# file encoder shortcut
encode(){
	if [ -z "$1" ]; then 
		echo "invalid argument"
	else
		python3 PATH/TO/PROJECT/encoder.py encode "$DIR/$1"
	fi
}

decode(){
	if [ -z "$1" ]; then 
		echo "invalid argument"
	else 
		python3 PATH/TO/PROJECT/encoder.py decode "$DIR/$1"
	fi
}
