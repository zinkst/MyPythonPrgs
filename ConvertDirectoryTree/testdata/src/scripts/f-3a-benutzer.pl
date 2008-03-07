#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


use lib qw(../lib);

use Person;


my @personen = 
   (
   Person->new("Hans Wurst",  "1970-01-01", "w"),     # $personen[0]
   Person->new("Tina Trulla", "1975-03-01", "w"),     #           1
   Person->new("Hutzel Hugo", "1980-01-05", "m"),     #           2
   );
   

foreach my $p (@personen)                             # schleife ueber alle Objekte
   {
            
   my $name       = $p->name;
   my $geschlecht = $p->geschlecht eq 'm' ? "maennlich" : "weiblich";
   my $geburtstag = $p->geburtstag;
   
   print "Benutzer '$name' ist $geschlecht und hat am $geburtstag Geburtstag. \n";
   
   my ($y, $m, $d) = $p->get_age;
   print "Damit ist er/sie/es $y Jahre, $m Monate, $d Tage alt\n\n";
   
   }








   