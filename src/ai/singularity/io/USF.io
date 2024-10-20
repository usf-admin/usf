/* Copyright 2024 Brian J. Zeien

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

->lib:io:default

USF:USF;

def Log(
	log_statement
) {
	:
		# ADD CODE HERE	
		ret 0;
	~->err
		# ADD CODE HERE
		ret 1, err;
}

def HandleError(
	problem_code, 
	problem_sub, 
	problem_description
) {
	:
		# ADD CODE HERE	
		ret 0;
	~->err
		# CODE HERE
		ret 1, err;
}
