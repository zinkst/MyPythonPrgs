#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use 5.010;

use IO::Prompt;

# ‹bersichtliche Variante:

my $anzahl_parameter = scalar @ARGV;
print "In der langen Variante wurde dieses Script mit $anzahl_parameter Parametern aufgerufen\n";

my $num = 1;
foreach my $parameter (@ARGV)
   {
   print "Parameter $num: $parameter\n";
   $num++;
   }


# Kurzvariante

print "\nHey Hoo, dieses Script wurde mit " . (scalar @ARGV) . " Parametern aufgerufen!\n";

print "  - $_\n" foreach @ARGV;


print "\n";

# Variante mit Shift
# shift holt sich (auﬂerhalb von Unterfunktionen) automatisch die Parameter aus ARGV

my $param;
print "  * $param\n" while $param = shift;


# === array2.pl ===================================

print "\nSooo, und nun geht es weiter: \n";

my @zahlen = ();

while (1)
   {
   my $zahl = prompt("Sag mir eine Zahl: ");
   
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
#my @neu = sort @zahlen;
$min = $neu[0];
$max = $neu[-1]; 


print "Variante 2: Die groesste Zahl ist $max, die kleinste $min\n";

 

# Variante 3 (foreach), hat einen ueberfluessigen Durchgang:

$min = $max = $zahlen[0];

foreach my $wert (@zahlen)
   {
   $min = $wert if $wert < $min;
   $max = $wert if $wert > $max;
   }

print "Variante 3: Die groesste Zahl ist $max, die kleinste $min\n";



# Variante 4, das einfachste von allen


use List::Util qw(min max);

$min = min(@zahlen);
$max = max(@zahlen);

print "Variante 4: Die groesste Zahl ist $max, die kleinste $min\n";


# Variante 5, zerstoert das Array, hat aber keine ueberfluessigen Durchgaenge:


$min = $max = shift @zahlen;                       # erstes Element rausschieben; das sind min und max!

while (defined(my $wert = shift @zahlen))          # alle verbliebenen Elemente durcharbeiten
   {
   $min = $wert if $wert < $min;
   $max = $wert if $wert > $max;
   }

print "Variante 5: Die groesste Zahl ist $max, die kleinste $min\n";





