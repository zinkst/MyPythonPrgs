#!/usr/bin/perl

use strict;
use warnings;



# Aufruf der Funktionen:

my $min = min(1, 2, 3, 9, 5, 7, 15, -1, 8);


# oder:

my @liste = (10, 20, -234, 236, 237, 83, 9, -1, 0, 999);


$min = min(@liste);                                # kein my, weil schon oben deklariert




print "Min Lang: " . min_langversion(@liste)   . "\n",
      "Min norm: " . min(@liste)               . "\n",
      "Max norm: " . max(@liste)               . "\n",
      "Avg:      " . avg(@liste)               . "\n",
      "Sum Schl: " . sum(101)                  . "\n",
      "Sum fast: " . sum_ohne_schleife(101)    . "\n";

sub min_langversion
   {
   my @liste = @_;
   my $min = shift @liste;
   
   foreach my $aktueller_wert (@liste)
      {
      $min = $aktueller_wert if $aktueller_wert < $min;
      }
   
   return $min;
   }


sub max_kurzversion
   {
   my $max = shift;
   $_ > $max and $max = $_ foreach @_;
   return $max;
   }


#
# mit Sort
#




sub min_langversion_sort
   {
   my @eingabe = @_;
   
   my @sortiert = sort {$a <=> $b} @eingabe;
   
   my $minimum = $sortiert[0];
   
   return $minimum;
   
   }





sub min
   {
   (sort {$a <=> $b} @_)[0];
   }

sub max
   {
   (sort {$a <=> $b} @_)[-1];
   }


use List::Util qw(min max);



# temporaeres Array shiften
sub max_temp
   {
   my @temp_array = sort {$b <=> $a} @_;
   return shift @temp_array;
   }

sub avg
   {
   my $sum = 0;
   
   $sum += $_ foreach @_;
   
   return $sum / scalar @_;
   
   }


# my $sum = sum($endwert);

sub sum
   {
   my $end = shift;
   
   my $sum = 0;
   
   for my $aktuelle_zahl (1..$end)
      {
      $sum += $aktuelle_zahl; 
      }
   
   # Oder: 
   # $sum += $_ for 1..$end;
   
   return $sum;
   
   }
   
   
sub sum_schneller
   {
   my $sum = 0;
   $sum += $_ for 1..$_[0];
   $sum;
   }




sub sum_ohne_schleife
   {
   my $zahl = shift;
   
   return ($zahl*($zahl+1))/2;
   
   }
  

  
  
  
  
  
 
 
 
 
 
 
 