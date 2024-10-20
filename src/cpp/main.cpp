/* Copyright 2010,2014,2019,2020,2023,2024 Brian J. Zeien

This file is part of Universal Software Framework (a.k.a USF).

USF is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

USF is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with USF.  If not, see <http://www.gnu.org/licenses/>.*/

#include "usf.h"

usf framework;

int main(int argc, char *argv[])
{
	if(framework.HandleArguments(argc, argv) == 0){
			
		if(framework.Setup() == 0){

			framework.Log(std::string("Getting data from file: ").append(framework.GetFilepathData()));
			StringArray array_data = framework.GetData(framework.GetFilepathData());

			for (unsigned int counter = 0; counter < array_data.size(); ++counter) {
				framework.Log(array_data[counter]);
			}

		} else {
			
			framework.HandleError(0, "main", "Setup failed.");
			return 1;
		}

		return 0;
		
	} else {
		
		return 1;
	}
}
