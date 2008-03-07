#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use IO::Prompt;


print qq(
Uebung 4B: Schleifen
=========

);



my $zufallszahl = int(rand(10)) + 1;
my $counter     = 1;

while (1)                                          # Endlosschleife 
   {
   $counter++;                                     # Zählt, wieviele Durchgänge wir haben.
   my $eingabe = prompt("Rate mal die Zufallszahl: ");
   
   last if $eingabe == $zufallszahl;               # beende Schleife wenn Zufallszahl und Eingabe gleich sind
   
   if ($zufallszahl < $eingabe)
      {
      print "Zum $counter. mal falsch geraten, Zufallszahl ist kleiner als $eingabe!\n";
      }
   else  
      {
      print "Zum $counter. mal falsch geraten, Zufallszahl ist groesser als $eingabe!\n";
      }
   $counter++;
   }


print "Glueckwunsch, nach $counter Versuchen erraten: die Zufallszahl ist tatsaechlich $zufallszahl!\n\n";


#
# Loesung mittels ?-Operator als abschreckendes Beispiel
# Funktioniert tadellos, ist sehr interessant -- aber natuerlich nicht sehr uebersichtlich
#
# (Dank an die Teilnehmer des Kurses vom 18. bis 21. September 2006 fuer diese wunderschöne Loesung! :-) )
#

{ # neuer Extrablock, dann kommen sich die Variablen nicht ins Gehege; nur noetig, weil hier alles in einer Datei steht
   
my $zufallszahl = int (rand (10)) + 1;
my $eingabe = 0;
my $versuche=1;

my $trash;   

while ($zufallszahl != $eingabe)
   { 
   $eingabe = prompt("Erraten Sie die Zufallszahl:");

   $trash = $zufallszahl == $eingabe 
      ? (print "Richtig erraten :-))\nBenoetigte Versuche: $versuche.\n")
      : ($zufallszahl < $eingabe
           ? (print "Falsch. Ihre Zahl ist zu gross.\n")
           : (print "Falsch. Ihre Zahl ist zu klein.\n")
        );

   $versuche++;
   } 

} # Ende des Extrablocks



# === summe.pl ====================================================

my $summe = 0;

while (1)                                          # Wieder eine Endlosschleife
   {
   my $zahl = prompt("Sag mal eine Zahl; Ende mit *: ");
   
   last if $zahl eq '';                            # Ende bei leerer Eingabe
   last if $zahl eq '*';                           # Ende mit *
   
   $summe += $zahl;
   
   }


print "Die Summe aller eingebenen Zahlen ist: $summe\n\n";



# === max.pl =====================================================




#
# Ausführliche Version
#

my $max = 0;
foreach my $i (1, 234, 123, 1234, 384, 19, 99, 15, 124)
   {
   if ($i > $max)
      {
      $max = $i;
      }
   }

print "Die groesste Zahl meiner (anderen eigenen) Liste ist: $max\n\n";


#
# knappere Version
#

$max = 0;
foreach my $i (1, 234, 123, 1234, 384, 19, 99, 15, 124)
   {
   $max = $i if $i > $max;
   }

print "Die groesste Zahl meiner Liste ist: $max\n\n";



# Hack-Version: alles in einer Zeile:

$max = 0;
$_ > $max and $max = $_ foreach 1, 234, 123, 1234, 384, 19, 99, 15, 124;

print "V3: Die groesste Zahl meiner Liste ist: $max\n\n";





#####

my $alter = 123;

$alter > 18 and print "Juchuu";

print "Juchuu" if $alter > 18;



#my $bedingung = 1;
#
#
#$bedingung and print "Hallo!\n";
#
#print "Hallo!\n" if $bedingung;








 

