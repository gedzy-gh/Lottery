#!/bin/bash
day=$(date +%A)
 if [ "$day" == "Thursday" ] || [ "$day" == "Sunday" ]; then
    msg="error";
    while [ $msg == "error" ]; do
        msg=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error)
        sleep 4s
    done
        sleep 4s
        notify-send -i "/home/$USER/PycharmProjects/The National Lottery/icon.png" -a "icon" "The National Lottery" "Crawling: https://www.national-lottery.co.uk/"
        python3 "/home/$USER/PycharmProjects/The National Lottery/main.py"
        exit 0 
    else
        exit 1
fi
