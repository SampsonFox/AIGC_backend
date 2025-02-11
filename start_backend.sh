#!/bin/bash
#gnome-terminal -t "pypy3" -x bash -c "pypy3;exec bash;"
{
	echo "Lunching pypy3"
	python3
}&

wait