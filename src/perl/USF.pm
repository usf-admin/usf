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

sub new {

	my $usf = {};
	$usf->{FILE_DATA} = "";
	$usf->{FILE_LOG} = "";
	$usf->{ID_LOG} = 0;
	$usf->{DELIMITER_LOG} = ",";
	bless($usf);
	return $usf;
}

sub file_data {

	my $usf = shift;
	if (@_) { $usf->{FILE_DATA} = shift }
	return $usf->{FILE_DATA};
}

sub file_log {

	my $usf = shift;
	if (@_) { $usf->{FILE_LOG} = shift }
	return $usf->{FILE_LOG};
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

	if ($problem_sub ne "Log") {

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
	my $path = $usf->file_log;
	my $id_log = ($usf->id_log + 1);	

	chomp($statement);
	
	if($path ne "") {

		eval {		

			if(open(LOGFILE, ">>$path")) {

				print LOGFILE ($statement . "\n");
	
			} else {
		
				print "Unable to open log file: " . $path . "\n";
				return 0;
			}
			close(LOGFILE);

		}; if ($@) { $usf->HandleError(0,"Log",$@); }
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

		print "Data file " . $path . " not found." . "\n";
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
		
		print "Unable to open data file: " . $path . "\n";
		return @return_array;
	}

	close(DATAFILE);
	return @return_array;
}
1;

