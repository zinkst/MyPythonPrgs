#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use Data::Dumper;

$| = 1;                                            # explizites Abschalten von Output-Buffering!

print qq(
Uebung 4B: Schleifen
=========

);


my $zufallszahl = int(rand(10)) + 1;
my $counter     = 1;

while (1)                                          # immer wahr, also Endlosschleife! 
   {
   
   print "Rate mal die Zufallszahl: ";
   my $eingabe = <STDIN>; chomp $eingabe;
   
   last if $eingabe == $zufallszahl;               # beende Schleife wenn ZUfallszahl und Eingabe gleich sind
   
   if ($zufallszahl < $eingabe)
      {
      print "Zum $counter. mal falsch geraten, Zufallszahl ist kleiner als $eingabe!\n";
      }
   else  
      {
      print "Zum $counter. mal falsch geraten, Zufallszahl ist groesser als $eingabe!\n";
      }
   $counter++;
   }


print "Glueckwunsch, nach $counter Versuchen erraten: die Zufallszahl ist tatsaechlich $zufallszahl!\n\n";

exit;

# === summe.pl ====================================================

my $summe = 0;

while (1)                                          # Wieder eine Endlosschleife
   {
   print "Sag mal eine Zahl; Ende mit *: ";
   my $zahl = <STDIN>; chomp $zahl;
   
   last if $zahl eq '*';                           # Ende mit *
   
   $summe += $zahl;
   
   }


print "Die Summe aller eingebenen Zahlen ist: $summe\n\n";



# === max.pl =====================================================

my $max = 0;

foreach my $i (1, 234, 123, 1234, 384, 19, 99, 15, 124)
   {
   $max = $i if $i > $max;
   }

print "Die groesste Zahl meiner Liste ist: $max\n\n";



foreach my $i (1, 234, 123, 1234, 384, 19, 99, 15, 124)
   {
   if ($i > $max)
      {
      $max = $i;
      }
   }

print "Die groesste Zahl meiner Liste ist: $max\n\n";





