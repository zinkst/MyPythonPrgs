#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


$|=1;                                              # Output Buffering ausschalten


use lib qw(../lib);                                # Anpassung des Modul-Suchpfades

use MyEncode;                                      # Einbinden des Moduls; alle automatisch 
                                                   # exportierten Symbole werden importiert
 

my $codiert = encode("Blafasel sagt irgendwer.", "qww");  # Aufruf der importierten Funktion "encode"

print "Kodiert:\n$codiert\n";

my $klartext = decode($codiert);                   # rufe das importierte Dekodieren auf.



print "Und Dekodiert ist der String: '$klartext'\n";





