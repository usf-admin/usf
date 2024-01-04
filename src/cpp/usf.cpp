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
	filepath_data = "";
	filepath_log = "";
	id_log = 0;
	delimiter_log = ",";
}

void usf::SetFileData(std::string filepath) { filepath_data = filepath; }
void usf::SetFileLog(std::string filepath) { filepath_log = filepath; }
void usf::SetIdLog(int id) { id_log = id; }
void usf::SetDelimiterLog(std::string delimiter) { delimiter_log = delimiter; }

void usf::HandleError(const int problem_code, std::string problem_sub, std::string problem_description)
{
	std::stringstream statement;

	statement << "ERROR" << usf::GetDelimiterLog() 
		  << problem_code << usf::GetDelimiterLog() 
		  << problem_sub << usf::GetDelimiterLog() 
		  << problem_description << std::endl;

	if(problem_sub.compare("Log") != 0) {

		usf::Log(statement.str());

	} else {

		std::cout << statement << std::endl;
	}
}

void usf::Log(std::string statement_log)
{
	usf::SetIdLog((usf::GetIdLog() + 1));

	std::string filepath_log = usf::GetFileLog();

	if(filepath_log.compare("") != 0) {

		try
		{

			std::ofstream logfile(filepath_log.c_str(), std::ios_base::out | std::ios_base::app);

			if (logfile.is_open()) {

			    logfile << statement_log << std::endl;

			} else {

			    usf::HandleError(0,"Log","Unable to open log file.");
			    return;
			}
			logfile.close();

		}
		catch(...) { usf::HandleError(0,"Log", "UNKNOWN"); }
	}

	std::cout << statement_log << std::endl;
}

StringArray usf::GetData(std::string filepath)
{
	StringArray return_array(0);

	try
	{
		if(!usf::VerifyFileExists(filepath)) {

			std::cout << "GetData(): Invalid data file path: " << filepath << "\n" << std::endl;
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

			std::cout << "GetData(): Unable to open data file: " << filepath << "\n" << std::endl;
			return return_array;
		}
	}
	catch(std::string ex) { std::cout << "GetData(): Unknown error:" << ex << "\n" << std::endl; }
	catch(...) { std::cout << "GetData(): Unknown error.\n" << std::endl; }
	return return_array;
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

usf::~usf()
{
	//destructor
}
