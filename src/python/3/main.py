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

def main():
	
	if framework.HandleArguments(argv_list=sys.argv) == 0:

		if framework.Setup() == 0:

			framework.Log(("Getting data from file: " + framework.Get_FilepathData()));
			    
			data = framework.GetData(framework.Get_FilepathData())
			
			for line in data:
				framework.Log(line.rstrip('\r\n'))

			return 0

		else:

			framework.HandleError(0, "main", "Setup failed.")
			return 1
			
	else:		
		return 1

main()
