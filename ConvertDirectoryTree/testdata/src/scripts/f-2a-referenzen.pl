#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


my $name1 = "Hutzel-Hugo";
my $name2 = "Wurzelgnom";

func1(\$name1, \$name2);


my @array1 = qw(Tina Tanja Tatjana Tante Trine);
my @array2 = (1,2,3,4,6,9,11);



# So sieht man es haeufig: Anonyme Arrays gleich als Referenzen
my $arrayref = [1,2,3,4,5,7,9,123];


func2(\@array1, \@array2);


sub func1
   {
   my ($name1_ref, $name2_ref) = @_;
      
   print "Name 1: $$name1_ref; Name 2: $$name2_ref\n";
   
   }


sub func2
   {
   my ($a1_ref, $a2_ref) = @_;
   
   print "Array 1: ", join(" - ", @$a1_ref), "\n";
   print "Array 2: ", join(" - ", @$a2_ref), "\n";
   
   }




####################################################################################
sleep 3;

# kompl_array.pl


my @a1 = (1,2,3);
my @a2 = (4,5,6,7);
my @a3 = qw(a b c);

my @referenzen = (\@a1, \@a2, \@a3);

my $str = @{ $referenzen[0] }[0];


print "Erstes Element erstes Array ist: @{$referenzen[0]}[0]\n";
print "Erstes Element erstes Array ist: $referenzen[0]->[0]\n";
print "Erstes Element erstes Array ist: $referenzen[0][0]\n";

print "Anzahl der Elemente in array 2 ist: " . scalar @{$referenzen[1]} . "\n";

print "Erstes Array enthaelt folgende Werte:\n";
print "  Wert: $_\n" foreach (@{ $referenzen[0] });






