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

my $framework = USF->new();

my $file_config = "/home/user1/code/usf/src/perl/main.conf";
my @array_config;
my $map_config = {};

main();

sub setup {

	my @properties;
	my $count_lines_config = 0;

	@array_config = $framework->GetData($file_config);
	$count_lines_config = scalar @array_config;

	if($count_lines_config > 0) {

		for(my $counter = 0; $counter < @array_config; $counter++) {

			if($array_config[$counter] ne "") {

				my(@chars_properties) = split //,$array_config[$counter];

				if($chars_properties[0] ne "#") {

					@properties = split /=/, $array_config[$counter];

					$map_config->{$properties[0]} = $properties[1];
				}
			}
		}

		$framework->file_log($map_config->{file_log});
		$framework->id_log(0);
		$framework->delimiter_log($map_config->{delimiter_log});
		$framework->file_data($map_config->{file_data});
		return 0;		

	} else {

		print "Empty config file: " . $file_config . "\n";
		return 1;
	}
}

sub main {

	my($rv_setup) = setup();
	if($rv_setup == 0) {

		$framework->Log(("Getting data from file: " . $framework->file_data()));
		my (@data) = $framework->GetData($framework->file_data());
		foreach (@data) {
			$framework->Log($_);
		}

		return 0;
	
	} else {

		print "Setup failed.\n";
		return 1;
	}
}
