#!/bin/bash
cd $2
vtune -collect memory-access -knob sampling-interval=1 --duration $1
cd -
