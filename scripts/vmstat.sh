#!/bin/bash
vmstat -n 1 $1 | awk '{ print strftime("%Y/%m/%d %H:%M:%S"), $0 } { system("") }' | sed -u -r 's/\s+/,/g' > $2/vmstat.csv
