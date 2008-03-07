#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

print "Hallo, ich starte!\n";


use English;
local $OUTPUT_AUTOFLUSH = 1;             # explizites Abschalten von Output-Buffering!

# geht auch mit: local $| = 1;


# Aufgabe 1: input.pl


print "Hallo, sag mal was! ";
my $sag = <STDIN>;
chomp $sag;

# chomp(my $input = <STDIN>);


print "Und bitte nenne mir eine Zahl: ";
my $zahl = <STDIN>;
chomp $zahl;



print "Und nun kommt $zahl mal <$sag>: " . ($sag x $zahl) . "\n";


# anders:
my $ausgabe = $sag x $zahl;
print "Und nun kommt $zahl mal <$sag>: $ausgabe\n";




# =====================================================================

# aufgabe 2 und 3

print "Sag mir Vorname! ";
my $vorname = <STDIN>; 
chomp $vorname;

print "Und der Nachname! ";
my $name = <STDIN>;
chomp $name;

print "PLZ? ";
my $plz = <STDIN>;
chomp $plz;

printf "| %20s | %20s | %10d\n",    $vorname, $name, $plz; 
printf "| %-20s | %-20s | %-10d\n", $vorname, $name, $plz; 

printf "| %30s | %10d\n",   "$vorname $name", $plz; 
printf "| %-30s | %-10d\n", "$vorname $name", $plz; 



# =======================================================================

# aufgabe 4

print "\n\nUnd nun kommt die Hex-Zahl!\n";

my $hex = sprintf "%04x", $zahl;
print "Zahl als Hex: $hex\n";

printf "Zahl als Hex: %04x\n", $zahl;



# Damit wir eine längere Hex-Zahl haben:
# das gleiche nochmal und mit Zahl*10 ausgeben

printf "$zahl als Hex ist: %04x; " . (10*$zahl) ." als hex ist: %04x\n",     $zahl,     $zahl*10;
#                          ^^^^     ^^^^^^^^^^^^                ^^^^^        ^^^^^^     ^^^^^^^^
#                       1. Format   Zahlenwert * 10           2. Format    1. Format   2. Format
#                      normale Zahl                           Zahl mal 10    Wert        Wert 
#
#      <-------- Baut einen großen Formatstring ---------------------->






# (hier) NICHT BENUTZT
sub prompt
   {
   local $| = 1;
   print $_[0];
   my $input = <STDIN>;
   chomp $input;
   return $input;
   }
















