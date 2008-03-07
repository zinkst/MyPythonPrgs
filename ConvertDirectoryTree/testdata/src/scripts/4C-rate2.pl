#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;


use IO::Prompt;


print qq(
Uebung 4C: Schleifen mit Block
=========

);



#
# Variante 1, nach Art der Musterloesung
#


my $zufallszahl = int(rand(10)) + 1;
my $counter     = 0;

SCHLEIFE: while (++$counter)                       # aeussere Schleife
   {
   my $eingabe = prompt("Rate mal die Zufallszahl: ");
   
   EXTRABLOCK:                                     # das hier ist der Block mit der Abfrage
      {
      $zufallszahl < $eingabe and do 
         {
         print "Zum $counter. mal falsch geraten, Zufallszahl ist kleiner als $eingabe!\n";
         last EXTRABLOCK;
         };
      $zufallszahl > $eingabe and do 
         {
         print "Zum $counter. mal falsch geraten, Zufallszahl ist groesser als $eingabe!\n";
         last EXTRABLOCK;
         };
      
      # Wenn nicht groesser und nicht kleiner: dann ist es gleich
      print "Glueckwunsch, nach $counter Versuchen erraten: die Zufallszahl ist tatsaechlich $zufallszahl!\n\n";
      last SCHLEIFE;
      
      }
   
   }






#
# Variante 2
#


print "\nNochmal, 2. Variante!\n\n";


my $zufallszahl = int(rand(10)) + 1;
my $counter     = 0;

while (++$counter)                                 # Counter ist immer wahr, also Endlosschleife! 
   {
   
   my $eingabe = prompt("Rate mal die Zufallszahl: ");
   
   ($eingabe == $zufallszahl) and last;            # beende Schleife wenn ZUfallszahl und Eingabe gleich sind
   
   EXTRABLOCK: 
      {
      ($zufallszahl < $eingabe) and do
         {
         print "Zum $counter. mal falsch geraten, Zufallszahl ist kleiner als $eingabe!\n";
         last EXTRABLOCK;
         };
         
      print "Zum $counter. mal falsch geraten, Zufallszahl ist groesser als $eingabe!\n";
      
      }                                            # end extrablock
   
   
   }


print "Glueckwunsch, nach $counter Versuchen erraten: die Zufallszahl ist tatsaechlich $zufallszahl!\n\n";


