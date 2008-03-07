#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
$| = 1;


my @module = qw(Blafasel5000 Blafasel5000::Super Irgendwas::Bla);


my $fehler = 0;

foreach my $modul (@module)
   {
   eval "use $modul;";
   if ($@)
      {
      print "FEHLER: Modul $modul nicht da!\n";
      $fehler = 1;
      }

   }
   

if ($fehler)
   {
   print "Programmstart abgebrochen\n\n";
   exit;
   }

   
   