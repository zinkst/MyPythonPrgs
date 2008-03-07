#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;


use IO::Prompt;


my $sag  = prompt("Hallo, sag mal was! ");
my $zahl = prompt("Und bitte nenne mir eine Zahl: ");


print "Und nun kommt $zahl mal '$sag': " . ($sag x $zahl) . "\n";



# =====================================================================


my $vorname = prompt("Sag mir Vorname! ");
my $name    = prompt("Und der Nachname! ");
my $plz     = prompt("PLZ? ");


printf "| %20s | %5i\n", "$vorname $name", $plz; 
printf "| %-20s | %-5i\n", "$vorname $name", $plz; 

printf "| %20s | %20s | %5i\n", $vorname, $name, $plz; 
printf "| %-20s | %-20s | %-5i\n", $vorname, $name, $plz; 



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






