#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

#
# Kurzvarianten
#

sub min
   {
   return (sort {$a <=> $b} @_)[0];
   }

sub max
   {
   return (sort {$b <=> $a} @_)[0];
   }


sub avg
   {
   my $sum = 0;
    
   $sum += $_ foreach @_;
   
   return $sum/(scalar @_);
   
   }


sub sum
   {
   my $endzahl = shift;
   
   my $sum = 0;
   
   $sum += $_ for 1..$endzahl;
   
   return $sum; 
   }



my @liste = (10, 20, 30, 1, -98, -9, -1, 1234, 99);


my $min = min(@liste);
my $max = max(@liste);
my $avg = avg(@liste);

print "Min: $min, Max: $max; Durchschnitt: $avg\n";


my $summe = sum($max);

print "Die Summe von 1 bis $max ist: $summe\n";


