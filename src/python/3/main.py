#!/usr/bin/env python

# Copyright 2010,2014,2019,2020,2023,2024 Brian J. Zeien

# This file is part of Universal Software Framework (a.k.a USF).

# USF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# USF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with USF.  If not, see <http://www.gnu.org/licenses/>.

from USF import *

framework = USF()

file_config = "/home/user1/code/usf/src/python/3/main.conf"
array_config = []
map_config = {}

def setup():

	try:

		array_config = framework.GetData(file_config)
		count_lines_config = len(array_config)

		if count_lines_config > 0:

			for line in array_config:

				if line != "":

					chars_properties = list(line)

					if chars_properties[0] != "#":

						properties = line.split("=")
						map_config[properties[0]] = properties[1].rstrip('\r\n')

			framework.Set_FileLog(map_config['file_log'])
			framework.Set_IdLog(0);
			framework.Set_DelimiterLog(map_config['delimiter_log']);
			framework.Set_FileData(map_config['file_data']);

		else:

			print("Empty config file: " + file_config)
			return 1

	except:

		ex = sys.exc_info() [0]
		framework.HandleError(0, "main.py->setup()", "%s" % ex)
		return 1

	return 0

def main():

	if setup() == 0:

		framework.Log(("Getting data from file: " + framework.Get_FileData()));
		data = framework.GetData(framework.Get_FileData())
		for line in data:
			framework.Log(line.rstrip('\r\n'))

		return 0

	else:

		print("Setup failed")
		return 1

main()
