#!/usr/bin/perl 

use strict;
use warnings;

use lib qw(/Users/alvar/workspace/Perl-Schulung/lib);

use Person;

# my $p0 = Person->new();


my $p1 = new Person ("Bettina Beispiel",   "1.1.1970", "w");
my $p2 = Person->new("Emma Example",       "2.1.1970", "w");
my $p3 = Person->new("Manfred Musterfrau", "3.1.1970", "m");


print 'Name von $p1 ist: ', $p1->name , "\n";
print 'Geburtstag von $p2 ist: ', $p2->geburtstag , "\n";
print 'Geschlecht von $p3 ist: ', $p3->geschlecht , "\n";





