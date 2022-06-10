#!/bin/bash
iostat -x 1 $1 -p sda,sdb | awk '{ print strftime("%Y/%m/%d %H:%M:%S"), $0 } { system("") }' | sed -u -r 's/\s+/,/g' > $2/iostat.csv
