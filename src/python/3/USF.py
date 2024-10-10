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

import sys
import datetime
import os

class USF:

	def __init__(self):
		
		self.relative_file_directory = os.path.dirname(os.path.abspath(__file__))
		self.default_filename_config = "usf.conf"
		self.filepath_config = ""
		self.filepath_data = ""
		self.filepath_log = ""
		self.id_log = 0
		self.delimiter_log = ","

	def Set_RelativeFileDirectory(self, relativefiledirectory): self.relative_file_directory = relativefiledirectory
	def Get_RelativeFileDirectory(self): return self.relative_file_directory
	def Set_FilepathConfig(self, filepathconfig): self.filepath_config = filepathconfig
	def Get_FilepathConfig(self): return self.filepath_config
	def Set_FilepathData(self, filepathdata): self.filepath_data = filepathdata
	def Get_FilepathData(self): return self.filepath_data
	def Set_FilepathLog(self, filepathlog): self.filepath_log = filepathlog
	def Get_FilepathLog(self): return self.filepath_log
	def Set_IdLog(self, idlog): self.id_log = idlog
	def Get_IdLog(self): return self.id_log
	def Set_DelimiterLog(self, delimiterlog): self.delimiter_log = delimiterlog
	def Get_DelimiterLog(self): return self.delimiter_log

	def HandleError(self, problem_code, problem_sub, problem_description):

		statement = "ERROR" + self.delimiter_log + str(problem_code) + self.delimiter_log + problem_sub + self.delimiter_log + problem_description;		

		if problem_sub != "Log" or problem_sub != "HandleArguments" or problem_sub != "Setup":

			self.Log(statement)

		else:			
			print(statement + "\n")

	def VerifyDirectoryExists(self, directory):

		if os.path.isdir(directory) == True:
			return 0

		else:
			return 1

	def VerifyFileExists(self, filepath):

		if os.path.isfile(filepath) == True:
			return 0

		else:
			return 1

	def Log(self, log_statement):

		path = self.filepath_log;
		self.id_log += 1

		try:

			log_statement.strip()

			if path != "":

				try:

					logfile = open(path,"a")

				except IOError:

					self.HandleError(0, "Log", "Unable to open log file.")
					return 1

				logfile.write((log_statement + "\n"))
				logfile.close()

			print(log_statement)

		except:

			ex = sys.exc_info() [0]
			self.HandleError(0, "Log", "%s" % ex)

		return 0

	def GetData(self, path):

		return_array = ("")

		try:

			if self.VerifyFileExists(path) != 0:

				self.HandleError(0, "GetData", "Invalid data file path.")
				return return_array

			try:

				datafile = open(path,"r")

			except IOError:

				self.HandleError(0, "GetData", "Unable to open data file.")
				return return_array

			return_array = datafile.readlines()
			datafile.close()

		except:
			
			ex = sys.exc_info() [0]
			self.HandleError(0, "GetData", "%s" % ex)

		return return_array
		
	def HandleArguments(self, argv_list):
		
		if len(argv_list) > 1:
			
			if self.VerifyFileExists(str(argv_list[1])) == 0:
				
				self.Set_FilepathConfig(str(argv_list[1]))
				return 0
				
			else:
				
				self.HandleError(0, "HandleArguments", ("Configuration file does not exist on absolute path: " + str(argv_list[1])))
				return 1
			
		else:
			
			relative_filepath_config = os.path.join(self.Get_RelativeFileDirectory(), self.default_filename_config)
			
			if self.VerifyFileExists(relative_filepath_config) == 0:
				
				self.Set_FilepathConfig(relative_filepath_config)
				return 0
				
			else:
				
				self.HandleError(0, "HandleArguments", ("Configuration file does not exist on relative path: " + relative_filepath_config))
				return 1
			
		print("usage: python main.py [filepath]\n")
		return 1
		
	def Setup(self):

		try:
			
			array_config = []
			map_config = {}		
								
			array_config = self.GetData(self.Get_FilepathConfig())
			count_lines_config = len(array_config)

			if count_lines_config > 0:

				for line in array_config:

					if line != "":

						chars_properties = list(line)

						if chars_properties[0] != "#":

							properties = line.split("=")
							map_config[properties[0]] = properties[1].rstrip('\r\n')

				self.Set_FilepathLog(map_config['filepath_log'])
				self.Set_IdLog(0);
				self.Set_DelimiterLog(map_config['delimiter_log']);
				self.Set_FilepathData(map_config['filepath_data']);

			else:

				self.HandleError(0, "Setup", ("Empty config file: " + self.Get_FilepathConfig()))
				return 1

		except:

			ex = sys.exc_info() [0]
			self.HandleError(0, "Setup", "%s" % ex)
			return 1

		return 0		
