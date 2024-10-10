#!/usr/bin/perl

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

use strict;
use USF;
use File::Basename;
use File::Spec;

my $framework = USF->new();

main();

sub main {
	
	if($framework->HandleArguments(\@ARGV) == 0) {
		
		if($framework->setup() == 0) {

			$framework->Log(("Getting data from file: " . $framework->filepath_data()));
			my (@data) = $framework->GetData($framework->filepath_data());
			foreach (@data) {
				$framework->Log($_);
			}

			return 0;
		
		} else {

			$framework->HandleError(0, "main", "Setup failed.");
			return 1;
		}
	
	} else {		
		return 1;
	}
}
