#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Antonio Martins (digiplan.pt@gmail.com)
#

import logging

def inside_level2():
	value = 3
	logging.warning("inside level 2 error %s", value)
	# value = 3/0
	raise RuntimeError("inside error (2)")
	
def inside_level1():
	inside_level2()
	logging.warning("inside level 1")
	# raise RuntimeError("inside error(1)")

#############################################################

logging.basicConfig(level=logging.INFO)

try:
	inside_level1()
except Exception as err:
	print("I caught an error: ", err.args)
print("Ending...")
