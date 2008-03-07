#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;                                            # explizites Abschalten von Output-Buffering!

# Kurzvariante

print "Hey Hoo, dieses Script wurde mit " . (scalar @ARGV) . " Parametern aufgerufen!\n";

print "  - $_\n" foreach @ARGV;


# Laengere Variante:

my $anzahl_parameter = @ARGV;
print "Auch in der langen Variante wurde dieses Script mit $anzahl_parameter Parametern aufgerufen\n";

my $num = 1;
foreach my $parameter (@ARGV)
   {
   print "Parameter $num: $parameter\n";
   $num++;
   }


# Variante mit Shift
# shift holt sich (auﬂerhalb von Unterfunktionen) automatisch die Parameter aus ARGV

my $param;
print "  * $param\n" while $param = shift;


# === array2.pl ===================================

print "\nSooo, und nun: ";

my @zahlen = ();

while (1)
   {
   print "Sag mir eine Zahl: ";
   my $zahl = <STDIN>; chomp $zahl;
   
   last if $zahl eq "" or $zahl eq "*";
   
   push @zahlen, $zahl;
   
   }



# Variante 1:

my $min = my $max = $zahlen[0];

for my $index (1..$#zahlen)
   {
   $min = $zahlen[$index] if $zahlen[$index] < $min;
   $max = $zahlen[$index] if $zahlen[$index] > $max;
   }

print "Variante 1: Die groesste Zahl ist $max, die kleinste $min\n";



# Variante 2:

my @neu = sort {$a <=> $b} @zahlen;
$min = $neu[0];
$max = $neu[-1]; 


print "Variante 2: Die groesste Zahl ist $max, die kleinste $min\n\n";

 

# Variante 3 (foreach), hat einen ueberfluessigen Durchgang:

$min = $max = $zahlen[0];

foreach my $wert (@zahlen)
   {
   $min = $wert if $wert < $min;
   $max = $wert if $wert > $max;
   }



# Variante 4, zerstoert das Array, hat aber keine ueberfluessigen Durchgaenge:


$min = $max = shift @zahlen;                       # erstes Element rausschieben; das sind min und max!

while (defined(my $wert = shift @zahlen))          # alle verbliebenen Elemente durcharbeiten
   {
   $min = $wert if $wert < $min;
   $max = $wert if $wert > $max;
   }

print "Variante 3: Die groesste Zahl ist $max, die kleinste $min\n\n";








