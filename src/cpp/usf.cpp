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

usf::usf()
{
	default_filename_config = "usf.conf";
	relative_file_directory = get_current_dir_name();
	filepath_config = "";
	filepath_data = "";
	filepath_log = "";
	id_log = 0;
	delimiter_log = ",";
}

void usf::SetRelativeFileDirectory(std::string relativefiledirectory) { relative_file_directory = relativefiledirectory; }
void usf::SetFilepathConfig(std::string filepath) { filepath_config = filepath; }
void usf::SetFilepathData(std::string filepath) { filepath_data = filepath; }
void usf::SetFilepathLog(std::string filepath) { filepath_log = filepath; }
void usf::SetIdLog(int id) { id_log = id; }
void usf::SetDelimiterLog(std::string delimiter) { delimiter_log = delimiter; }

void usf::HandleError(const int problem_code, std::string problem_sub, std::string problem_description)
{
	std::stringstream statement;

	statement << "ERROR" << usf::GetDelimiterLog() 
		  << problem_code << usf::GetDelimiterLog() 
		  << problem_sub << usf::GetDelimiterLog() 
		  << problem_description;

	if(problem_sub.compare("Log") != 0) {

		usf::Log(statement.str());

	} else {

		std::cout << statement << std::endl;
	}
}

int usf::VerifyDirectoryExists(std::string directory)
{
	DIR *t_dir;
	if ((t_dir = opendir(directory.c_str())) == NULL ) {
		return 0;

	} else {

		closedir(t_dir);
		return 1;
	}
}

int usf::VerifyFileExists (std::string filepath) 
{
	if (FILE *file = fopen(filepath.c_str(), "r")) {

		fclose(file);
		return 1;

	} else {

		return 0;
	}
}

void usf::Log(std::string statement_log)
{
	usf::SetIdLog((usf::GetIdLog() + 1));

	std::string filepath_log = usf::GetFilepathLog();

	if(filepath_log.compare("") != 0) {

		try
		{

			std::ofstream logfile(filepath_log.c_str(), std::ios_base::out | std::ios_base::app);

			if (logfile.is_open()) {

			    logfile << statement_log << std::endl;

			} else {

			    usf::HandleError(0, "Log", "Unable to open log file.");
			    return;
			}
			logfile.close();

		}
		catch(...) { usf::HandleError(0, "Log", "UNKNOWN"); }
	}

	std::cout << statement_log << std::endl;
}

StringArray usf::GetData(std::string filepath)
{
	StringArray return_array(0);

	try
	{
		if(!usf::VerifyFileExists(filepath)) {
			
			usf::HandleError(0, "GetData", ("Invalid data file path: " + filepath + "\n"));
			return return_array;
		}

		std::string dataline;
		std::ifstream datafile(filepath.c_str());

		if (datafile.is_open()) {

			while (getline(datafile,dataline)) {
				return_array.push_back(dataline);
			}

			datafile.close();

		} else {
						
			usf::HandleError(0, "GetData", ("Unable to open data file: " + filepath + "\n"));
			return return_array;
		}
	}
	catch(std::string ex) { usf::HandleError(0, "GetData", ("Unknown error: " + ex + "\n")); }
	catch(...) { usf::HandleError(0, "GetData", "Unknown error"); }
	return return_array;
}

int usf::HandleArguments(int argc, char *argv[])
{
	if(argc > 1){
			
		if(usf::VerifyFileExists(argv[1])) {

			usf::SetFilepathConfig(argv[1]);
			return 0;
		
		} else {
			
			usf::HandleError(0, "HandleArguments", ("Configuration file does not exist on absolute path: " + std::string(argv[1])));
			return 1;
		}		
		
	} else {
		
		std::string relative_filepath_config = (usf::GetRelativeFileDirectory() + "/" + usf::GetDefaultFilenameConfig());
		
		if(usf::VerifyFileExists(relative_filepath_config)) {

			usf::SetFilepathConfig(relative_filepath_config);
			return 0;
		
		} else {
			
			usf::HandleError(0, "HandleArguments", ("Configuration file does not exist on relative path: " + relative_filepath_config));
			return 1;
		}
	}
	
	std::cout << "usage: ./test_framework [filepath]" << std::endl;
	return 1;
}

int usf::Setup()
{
	
	StringArray array_config(0);
	int count_lines_config = 0;	
	StringArray properties(0);
	std::tr1::unordered_map<std::string, std::string> map_config;	

	array_config = usf::GetData(usf::GetFilepathConfig());
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

		usf::SetFilepathLog(map_config["file_log"]);
		usf::SetIdLog(0);
		usf::SetDelimiterLog(map_config["delimiter_log"]);
		usf::SetFilepathData(map_config["file_data"]);
		return 0;

	} else {
		
		usf::HandleError(0, "Setup", ("Empty config file: " + usf::GetFilepathConfig()));
		return 1;
	}
}

usf::~usf()
{
	//destructor
}
