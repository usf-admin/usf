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

package USF;
use strict;
use Cwd;

sub new {

	my $usf = {};
	my($path_filename, $path_dirs, $path_suffix) = File::Basename::fileparse(Cwd::abs_path(__FILE__));
	$usf->{DEFAULT_FILENAME_CONFIG} = "usf.conf";
	$usf->{RELATIVE_FILE_DIRECTORY} = $path_dirs;
	$usf->{FILEPATH_CONFIG} = "";
	$usf->{FILEPATH_DATA} = "";
	$usf->{FILEPATH_LOG} = "";
	$usf->{ID_LOG} = 0;
	$usf->{DELIMITER_LOG} = ",";
	bless($usf);
	return $usf;
}

sub default_filename_config {

	my $usf = shift;
	if (@_) { $usf->{DEFAULT_FILENAME_CONFIG} = shift }
	return $usf->{DEFAULT_FILENAME_CONFIG};
}

sub relative_file_directory {

	my $usf = shift;
	if (@_) { $usf->{RELATIVE_FILE_DIRECTORY} = shift }
	return $usf->{RELATIVE_FILE_DIRECTORY};
}

sub filepath_config {

	my $usf = shift;
	if (@_) { $usf->{FILEPATH_CONFIG} = shift }
	return $usf->{FILEPATH_CONFIG};
}

sub filepath_data {

	my $usf = shift;
	if (@_) { $usf->{FILEPATH_DATA} = shift }
	return $usf->{FILEPATH_DATA};
}

sub filepath_log {

	my $usf = shift;
	if (@_) { $usf->{FILEPATH_LOG} = shift }
	return $usf->{FILEPATH_LOG};
}

sub delimiter_log {

	my $usf = shift;
	if (@_) { $usf->{DELIMITER_LOG} = shift }
	return $usf->{DELIMITER_LOG};
}

sub id_log {

	my $usf = shift;
	if (@_) { $usf->{ID_LOG} = shift }
	return $usf->{ID_LOG};
}

sub HandleError {

	my $usf = shift;
	my $problem_code = $_[0];
	my $problem_sub = $_[1];
	my $problem_description = $_[2];
	my $statement = "ERROR" . $usf->delimiter_log . 
					$problem_code . $usf->delimiter_log . 
					$problem_sub . $usf->delimiter_log . 
					$problem_description;

	if ($problem_sub ne "Log" || $problem_sub ne "HandleArguments" || $problem_sub ne "Setup") {

		$usf->Log($statement); 

	} else {

		chomp($statement);
		print $statement . "\n";
	}
}

sub VerifyDirectoryExists {

	my $usf = shift;
	my $directory = $_[0];

	if(-d $directory) {
		return 1;
	} else {
		return 0;
	}
}

sub VerifyFileExists {

	my $usf = shift;
	my $path = $_[0];

	if(-e $path) {
		return 1;
	} else {
		return 0;
	}
}

sub Log {

	my $usf = shift;
	my $statement = $_[0];
	my $path = $usf->filepath_log;
	my $id_log = ($usf->id_log + 1);	

	chomp($statement);
	
	if($path ne "") {

		eval {		

			if(open(LOGFILE, ">>$path")) {

				print LOGFILE ($statement . "\n");
	
			} else {
		
				$usf->HandleError(0, "Log", ("Unable to open log file: " . $path));
				return 0;
			}
			close(LOGFILE);

		}; if ($@) { $usf->HandleError(0, "Log", $@); }
	}	

	print $statement . "\n";
	return 1;
}

sub GetData {

	my $usf = shift;
	my $path = $_[0];
	my @return_array;
	my $temp = "";
	my $counter_data_rows = 0;

	if(!$usf->VerifyFileExists($path)) {

		$usf->HandleError(0, "GetData", "Invalid data file path.");
		return @return_array;
	}
	
	if(open(DATAFILE, $path)) {

		while (<DATAFILE>) {
			$temp = $_;
			chomp($temp);
			$return_array[$counter_data_rows] = $temp;
			$counter_data_rows++;
		}
		close(DATAFILE);

	} else {
		
		$usf->HandleError(0, "GetData", "Unable to open data file.");
		return @return_array;
	}

	close(DATAFILE);
	return @return_array;
}

sub HandleArguments {
	
	my $usf = shift;
	my @argv_list = @{$_[0]};
	
	if((scalar @argv_list) > 0) {
		
		if($usf->VerifyFileExists($argv_list[0])) {
			
			$usf->filepath_config($argv_list[0]);
			return 0;
		
		} else { 
			
			$usf->HandleError(0, "HandleArguments", "Configuration file does not exist on absolute path: " . $argv_list[0]);
			return 1;
		}
		
	} else {
				
		# With non-unix remember to set $volume parameter for catpath appropriately ("C:", "D:", etc)
		my $relative_filepath_config = File::Spec->catpath("", $usf->relative_file_directory(), $usf->default_filename_config());
		
		if($usf->VerifyFileExists($relative_filepath_config)) {
			
			$usf->filepath_config($relative_filepath_config);
			return 0;
		
		} else { 
			
			$usf->HandleError(0, "HandleArguments", "Configuration file does not exist on relative path: " . $relative_filepath_config);
			return 1;
		}		
	}
	
	print "usage: python main.py [filepath]\n";
	return 1;		
}

sub setup {

	my $usf = shift;
	my @array_config;
	my $count_lines_config = 0;
	my @properties;
	my $map_config = {};
		
	@array_config = $usf->GetData($usf->filepath_config());
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

		$usf->filepath_log($map_config->{file_log});
		$usf->id_log(0);
		$usf->delimiter_log($map_config->{delimiter_log});
		$usf->filepath_data($map_config->{file_data});
		return 0;		

	} else {
		
		$usf->HandleError(0, "setup", ("Empty config file: " . $usf->filepath_config() . "\n"));
		return 1;
	}
}
1;
