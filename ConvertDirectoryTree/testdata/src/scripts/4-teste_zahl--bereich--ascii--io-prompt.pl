#!/usr/bin/perl

#
# Aufgabe 4A
# diese variante gelöst mit IO::Prompt
#

use warnings;
use strict;
use diagnostics;

use IO::Prompt;


my $zahl1 = prompt("Bitte nenne mir eine Zahl: ");
my $zahl2 = prompt("Bitte nenne mir noch eine Zahl: ");


if ($zahl1 < $zahl2)
   {
   print "Die erste Zahl ($zahl1) ist kleiner als die zweite ($zahl2)\n";
   }
elsif ($zahl1 > $zahl2)
   {
   print "Die erste Zahl ($zahl1) ist groesser als die zweite ($zahl2)\n";
   }
else
   {
   print "Beide Zahlen sind gleich gross ($zahl2)\n";
   }


# =======================================================================



my $zahl = prompt("Bitte nenne mir eine Zahl zwischen 1 und 12: ");

# Variante 1:
if ($zahl >= 1 and $zahl <= 12)
   {
   print "Die Zahl ($zahl) ist korrekt\n";
   }
else
   {
   print "Die Zahl ($zahl) ist NICHT korrekt.\n";
   }



# variante 2
print "Die Zahl ist ";
print "NICHT " unless ($zahl >= 1 and $zahl <= 12);
print "korrekt.\n";


# Variante 3
print "Die Zahl ist " . (($zahl >= 1 and $zahl <= 12) ? "" : "NICHT ") . "korrekt.\n";


# Variante 4
my $nicht = "";
$nicht = " NICHT" unless ($zahl >= 1 and $zahl <= 12);
print "Die Zahl ist$nicht korrekt.\n";


print "\n";


# =======================================================================

my $string_1 = prompt("Sag was! ");
my $string_2 = prompt("Sag nochmal was! ");


if ($string_1 lt $string_2)
   {
   print "Der erste String '$string_1' ist kleiner als der zweite '$string_2'\n";
   }
elsif ($string_1 gt $string_2)
   {
   print "Die erste String '$string_1' ist groesser als der zweite '$string_2'\n";
   }
else
   {
   print "Beide Strings sind identisch: '$string_1'\n";
   }



