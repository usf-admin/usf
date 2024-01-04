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

#ifndef USF_H
#define USF_H

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <tr1/unordered_map>
#include <time.h>
#include <dirent.h>

typedef std::vector<std::string> StringArray;

class usf
{
	protected:
	private:

		std::string filepath_data;
		std::string filepath_log;
		int id_log;
		std::string delimiter_log;

	public:

        	usf();

		void SetFileData(std::string filepath);
		void SetFileLog(std::string filepath);
		void SetIdLog(int id);
		void SetDelimiterLog(std::string filepath);
		std::string GetFileData() { return filepath_data; }
		std::string GetFileLog() { return filepath_log; }
		int GetIdLog() { return id_log; }
		std::string GetDelimiterLog() { return delimiter_log; }
		void Log(std::string statement);
		StringArray GetData(std::string filepath);
		int VerifyDirectoryExists(std::string directory);
		int VerifyFileExists (std::string filepath);
		void HandleError(const int problem_code, std::string problem_sub, std::string problem_description);

        virtual ~usf();
};

#endif // USF_H

