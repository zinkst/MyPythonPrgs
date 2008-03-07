#!/usr/bin/perl

use strict;
use warnings;


#for (1..3)
#   {
   
   my $zk = "Hallo!!!\n\n\n";
   my $anzahl = 0;
   
   
   {
      
      my $nl = chomp $zk;
      if ($nl) 
         {
         $anzahl++;
         redo;
         }
      else
         {
         print "Jetzt sind $anzahl Newlines Weg!\nEnde.\n";
         }
      
   }
   
 #  }