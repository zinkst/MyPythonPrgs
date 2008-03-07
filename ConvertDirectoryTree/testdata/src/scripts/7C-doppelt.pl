#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;                                            # explizites Abschalten von Output-Buffering!


while (1)
   {
   print "Gebe mal was ein, und ich suche nach Dopplern: ";
   
   my $eingabe = <STDIN>;
   chomp $eingabe;
   
   if ($eingabe =~ /\b(\w+)\b.*\b\1\b/)
      {
      print "Ja, mindestens ein Wort kommt doppelt vor, und zwar: '$1'!\n";
      }
   else
      {
      print "Nix doppelt\n";
      }
   
   }





