#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;                                # explizites Abschalten von Output-Buffering!


print "Bitte nenne mir eine Zahl: ";
my $zahl1 = <STDIN>;
chomp $zahl1;

print "Bitte nenne mir noch eine Zahl: ";
my $zahl2 = <STDIN>;
chomp $zahl2;


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



print "Bitte nenne mir eine Zahl zwischen 1 und 12: ";
my $zahl = <STDIN>;
chomp $zahl;


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
print "Die Zahl ist "  . (($zahl >= 1 and $zahl <= 12) ? "" : "NICHT ") . "korrekt.\n";

# Variante 4
my $nicht = "";
$nicht =  " NICHT" unless ($zahl >= 1 and $zahl <= 12);
print "Die Zahl ist$nicht korrekt.\n";




# =======================================================================

my $a = "kkhjg";
my $b = "kdsjhf";


if ($a lt $b)
   {
   print "Der erste String '$a' ist kleiner als der zweite '$b'\n";
   }
elsif ($a gt $b)
   {
   print "Die erste String '$a' ist groesser als der zweite '$b'\n";
   }
else
   {
   print "Beide Strings sind identisch: '$a'\n";
   }



