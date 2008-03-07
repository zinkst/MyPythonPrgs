#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;                                            # explizites Abschalten von Output-Buffering!

#
#


#
# oder als Perl-Einzeiler: (siehe auch: perldoc perlrun)
# 
#   perl -i.bak -npe 's/:/|/g' *.txt
#


print "\n\n";

my @buecher;

while (<>)                                         # Einlesen der Datei die auf der Kommandozeile angegeben wurde.
   {
   push @buecher, $_;                              # fuer Teil zwei Zeischenspeichern
   
   s/:/|/g;                                        # Suchen und Ersetzen in der Allerweiltvariable
   print;                                          # Ergebnis ausgeben
   
   }


#
# Aufgabe 2, prtbuch2.pl
#

# 3-486-21514-0:Lexikon der Informatik:Verlag R. Oldenburg:Schneider, Hans-Jochen:99.70:1011

# $isbn        $titel                 $verlag             $autor                 .....

# [^:]+          [^:]+                 [^:]+              [^:]+

print "\n\n";



foreach my $buch (@buecher)
   {
   my ($isbn, $titel, $verlag, $autor) = $buch =~ 
      m(
      ^([^:]+)
      :
       ([^:]+)
      :
       ([^:]+)
      :
       ([^:]+)
      )x;
   
   printf "%-14s | %-44s | %-20s\n", $isbn, $titel, $autor;
   
   }





print "\n\n";


#
# Variante mit Split (sh naechstes Kapitel)
#

foreach my $buch (@buecher)
   {
   my ($isbn, $titel, $verlag, $autor) = split(/:/, $buch);
   printf "%-14s | %-44s | %-20s\n", $isbn, $titel, $autor;
   
   }



print "\n\n";






