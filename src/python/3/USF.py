#!/usr/bin/env python

# Copyright2010,2014,2019,2020,2023,2024 Brian J. Zeien

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

		self.file_data = ""
		self.file_log = ""
		self.id_log = 0
		self.delimiter_log = ","

	def Set_FileData(self, filedata): self.file_data = filedata
	def Get_FileData(self): return self.file_data
	def Set_FileLog(self, filelog): self.file_log = filelog
	def Get_FileLog(self): return self.file_log
	def Set_IdLog(self, idlog): self.id_log = idlog
	def Get_IdLog(self): return self.id_log
	def Set_DelimiterLog(self, delimiterlog): self.delimiter_log = delimiterlog
	def Get_DelimiterLog(self): return self.delimiter_log

	def HandleError(self, problem_code, problem_sub, problem_description):

		statement = "ERROR" + self.delimiter_log + str(problem_code) + self.delimiter_log + problem_sub + self.delimiter_log + problem_description;		

		if problem_sub != "Log":

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

		path = self.file_log;
		self.id_log += 1

		try:

			log_statement.strip()

			if path != "":

				try:

					logfile = open(path,"a")

				except IOError:

					self.HandleError(0,"Log","Unable to open log file.")
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

				self.HandleError(0,"GetData","Invalid data file path.")
				return return_array

			try:

				datafile = open(path,"r")

			except IOError:

				self.HandleError(0,"GetData","Unable to open data file.")
				return return_array

			return_array = datafile.readlines()
			datafile.close()

		except:
			ex = sys.exc_info() [0]
			self.HandleError(0, "GetData", "%s" % ex)

		return return_array
