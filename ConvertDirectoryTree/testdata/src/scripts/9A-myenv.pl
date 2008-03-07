#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;    # explizites Abschalten von Output-Buffering!


 goto WOERTER;

#goto TEST;


#
# 1) myenv.pl
#


# Kurzversion ohne Plausibilitätstests

print "Die Environment-Variable $ARGV[0] ist definiert als $ENV{$ARGV[0]}\n";

use 5.010;

# Ausfuehrliche Version:

my $variable = shift // die "Fehler: kein Parameter Uebergeben!";

my $wert = $ENV{$variable} // "<undefiniert>";    # /
#$wert = "<undefiniert>" unless defined $wert;


print "Die Environment-Variable $variable ist definiert als $wert\n";

# (Problem mit Environment-Variablen mit Wert "0" oder Leerstring)



# ============================================================================


# 2) kennz.pl

my $superkennz = "xx"; # prompt("Was ist superkennzeichen?");


my %kennzeichen_tabelle = (
   S               => "Stuttgart",           # kommentar
   ES              => "Esslingen",
   B               => "Berlin",
   HH              => "Hamburg",
   F               => "Frankfurt am Main",
   M               => "Muenchen",
   uc($superkennz) => "Superstadt",

   # ...
                          );


while (1)
   {

   print "Hay Hoo, bitte gebe ein Kennzeichen ein: ";

   my $kennzeichen = <STDIN>;
   chomp $kennzeichen;

   last if $kennzeichen eq "" or $kennzeichen eq "*";

   if (my $ort = $kennzeichen_tabelle{ uc($kennzeichen) })
      {
      print "Ja, gefunden: Zum Kennzeichen $kennzeichen gehoert der Ort $ort\n";
      }
   else
      {
      print "Kennzeichen nicht gefunden\n";
      }

   } ## end while (1)


use Data::Dumper;

print "\nMeine Kennzeichen-Tabelle war: \n";
print Dumper(\%kennzeichen_tabelle);


# =====================================================================

# ...
#
# woerter.pl
#

WOERTER:

my %woerter;

while (1)
   {

   print "Guten Tach, sag mir mal ein Wort, oder auch mehrere: ";

   $_ = <STDIN>;    # diesmal mit der allerweltsvariablen
   chomp;

   last if $_ eq "*";    # or $_ eq "*";
   next if $_ eq "";

   $woerter{ lc($_) }++
      foreach split /\W+/;    # wenn mehrere, dann splitte an nicht-Buchstaben/Zahlen auf
                              # und addiere eins drauf im Hash mit den Woertern als Key

=for lang
   # $_: "GUten Tag ich bin ein Test."
   my @woerter = split(/\W+/, $_);
   foreach my $wort (@woerter)
      {
      my $klein = lc($wort);
      unless (defined $woerter{$klein})
         {
         $woerter{$klein} = 1;
         }
      else
         {
         $woerter{$klein}++;
         }
      }
   
=cut


   } ## end while (1)


foreach my $key (sort { $woerter{$b} <=> $woerter{$a} } keys %woerter)
   {
   printf "Wort: %16s, Haeufigkeit: %2d\n", $key, $woerter{$key};
   }


print "Verschiedene Woerter: " . (scalar keys %woerter) . "\n";


######################################################

TEST:

my @eingegebene_namen = ();    # irgendwoher

my %verbotene_namen = map { lc($_) => 1 } qw(Marie-Luise Kevin Mandy Paul);



use Data::Dumper;

print Dumper(\%verbotene_namen);


foreach my $name (@eingegebene_namen)
   {
   if ($verbotene_namen{$name})
      {
      print "IIiiih, $name ist verboten!\n";
      }
   }



