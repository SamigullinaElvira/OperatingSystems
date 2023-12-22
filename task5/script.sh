#!/bin/bash

RED='\e[31m'
GREEN='\e[32m'
RESET='\e[0m'

declare step_counter=0
declare hit_counter=0
declare numbers

while true; do
    secret_number=${RANDOM: -1}
    
    ((step_counter++))

    echo "Step: ${step_counter}"

    read -p "Please enter number from 0 to 9 (q - quit): " input

    case "$input" in
	[qQ])
	    echo "Bye! Exit..."
    	    exit 0
	;;

	[0-9])
	    if [[ "$input" == "$secret_number" ]]; then
	    	((hit_counter++))
    		echo "Hit! My number: ${secret_number}"
		number_string="${GREEN}${secret_number}${RESET}"
	    else
		echo "Miss! My number: ${secret_number}"
		number_string="${RED}${secret_number}${RESET}"
	    fi

	    numbers+=("${number_string}")

	    let hit_percent=(hit_counter * 100 / step_counter)
	    let miss_percent=(100 - hit_percent)    

	    echo "Hit: ${hit_percent}%" "Miss: ${miss_percent}%"

	    if (( ${#numbers[@]} > 10 )); then
	        echo -e "Last 10 items: ${numbers[@]: -10}"
	    else
	        echo -e "Last 10 items: ${numbers[@]} "	    

	    fi
	    ;;

	    *)
		echo "Not valid input. Please repeat"
    		((step_counter--))
	    ;;
    esac

    echo

done
