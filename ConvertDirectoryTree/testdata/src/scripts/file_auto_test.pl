#!/usr/bin/perl


use strict;
use warnings;

my $line = 1;

# open FILE, shift or die "Datei Fehler: $!";


while (<>)
   {
   print "$line: $_";
   $line++;
   }


# close FILE;







