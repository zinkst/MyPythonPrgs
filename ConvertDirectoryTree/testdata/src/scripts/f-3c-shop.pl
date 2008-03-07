#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


use lib qw(../lib);

use Person::Verkaeufer;


my @verkaeufer = 
   (
   Person::Verkaeufer->new("Hans Wurst",  "1970-01-01", "w", 1234),     # $personen[0]
   Person::Verkaeufer->new("Tina Trulla", "1975-03-01", "w", 2345),     #           1
   Person::Verkaeufer->new("Hutzel Hugo", "1980-01-05", "m", 3456),     #           2
   );
   

foreach my $p (@verkaeufer)                             # schleife ueber alle Objekte
   {
            
   my $name       = $p->name;
   my $geschlecht = $p->geschlecht eq 'm' ? "maennlich" : "weiblich";
   my $geburtstag = $p->geburtstag;
   my $gehalt     = $p->gehalt;
   
   
   print "$name bekommt $gehalt\n";
   
   
   }








   