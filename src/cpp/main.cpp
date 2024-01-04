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

std::string file_config = "/home/user1/code/usf/src/cpp/main.conf";
StringArray array_config(0);
std::tr1::unordered_map<std::string, std::string> map_config;

int setup();

int main()
{
	if(setup() == 0){

		framework.Log(std::string("Getting data from file: ").append(framework.GetFileData()));
		StringArray array_data = framework.GetData(framework.GetFileData());

		for (unsigned int counter = 0; counter < array_data.size(); ++counter) {
			framework.Log(array_data[counter]);
		}

	} else {

		std::cout << "Setup failed." << std::endl;
		return 1;
	}

    return 0;
}

int setup()
{
	StringArray properties(0);
	int count_lines_config = 0;

	array_config = framework.GetData(file_config);
	count_lines_config = array_config.size();

	if(count_lines_config > 0) {

	    for (unsigned int counter = 0; counter < array_config.size(); ++counter) {

		if(array_config[counter].compare("") != 0) {

			if(std::string(1,array_config[counter].at(0)).compare("#") != 0) {

				std::stringstream tempStream(array_config[counter]);
				std::string string_token;

				while(std::getline(tempStream, string_token, '=')) {
					properties.push_back(string_token);
				}

				map_config[properties[0]] = properties[1];
					properties.clear();
				}
			}
		}

		framework.SetFileLog(map_config["file_log"]);
		framework.SetIdLog(0);
		framework.SetDelimiterLog(map_config["delimiter_log"]);
		framework.SetFileData(map_config["file_data"]);
		return 0;

	} else {

		std::cout << "Empty config file: " << file_config << std::endl;
		return 1;
	}
}
