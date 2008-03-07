#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;


my $variable = "hallo";
#print $variabel;


print "Hallo Welt!\n";

print "Hallo \"Welt\"!\n";


print "\n\t\tHallo Welt!\n";


print '\n\t\tHallo Welt!\n';


#
# Es gibt auch noch weitere Quoting-Operatoren
# Damit kann man sich das lästige Maskieren mit \ ersparen, 
# wenn man innerhalb eines Textes Begrenzungszeichen benötigt
#
# siehe auch: perldoc perlop
#

print qq(Hallo "Welt"!\n);
print qq/Hallo "Welt"!\n/;
print qq{Hallo "Welt"!\n};
print qq(Hallo ("Welt")!\n);

print qq[Hallo ("Welt"!\n];



# STATUS="ERROR $err"
my $err = 123;
print qq(STATUS="ERROR $err");

print "STATUS=\"ERROR " . $err . "\"";



print qq(\n\t\tHallo Welt!\n);


print q(\n\t\tHallo 'Welt'!\n);

print "\n\n";


