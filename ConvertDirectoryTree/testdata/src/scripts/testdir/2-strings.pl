



#!/usr/bin/perl -w -T

use warnings;
use strict;
use diagnostics;


my $var1 = "Blafasel!";
my $var2 = "Blablubb.";
my $var3 = $var1 . $var2;

my $var3b = "$var1$var2";    # weniger übersichtlich, aber intern das gleiche


print "Variable 3 lautet: '$var3'\n";

my $farbe  = "rot";
my $anzahl = 4;


print "\n\n";
print $farbe x $anzahl;
print "\n\n";

print "'$farbe' $anzahl mal ausgegeben ist: " . ($farbe x $anzahl) . "\n";

sleep 2;

# =========================================================================


# Aufgabe 2

my $i = 40;
my $j = ($i += 4);

print "\$i hat den wert $i; \$j hat den Wert $j\n";

#
# Besser und übersichtlicher (und damit robuster)
# wäre der Code so:
#

my $i2 = 40;
$i2 += 4;
my $j2 = $i2;



# Aufgabe 3


my $k = 99;
my $l = $k++;


print "\$k hat den Wert $k; \$l hat den Wert $l\n";



#######################################

$i = 123;


# das in eine Zeile
$i = $i + 1;
print "Zahl = $i\n";


$i++;
print "Zahl = $i\n";

++$i;
print "Zahl = $i\n";


# i: 126

print "Zahl = " . (++$i) . "\n";

#      Zahl = 127\n


print "Zahl = " . ++$i . "\n";


print "Zahl = " . $i++ . "\n";



print "Zahl+1 = " . ($i + 1) . "\n";



