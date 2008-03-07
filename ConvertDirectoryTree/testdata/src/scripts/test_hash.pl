#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

$| = 1;                                            # explizites Abschalten von Output-Buffering!



my %personen =
   (
   "tina mueller"     =>   {
                           personal_nummer   => 12345,
                           geb_tag           => "1970-01-01",
                           gehalt            => 12345,
                           abteilung         => "3e",
                           schulungen        => [qw(perl shell c)],
                           },
   "hansi gnom"     =>   {
                           personal_nummer   => 1245,
                           geb_tag           => "1970-01-01",
                           gehalt            => 1345,
                           abteilung         => "2e",
                           schulungen        => [qw(10finger telefondienst)],
                           },
   
   "tina trulla"     =>   {
                           personal_nummer   => 1247,
                           geb_tag           => "1970-01-01",
                           gehalt            => 13454,
                           abteilung         => "1e",
                           schulungen        => [qw(hausmeisterdienst)],
                           },
   "martin mayer"     =>   {
                           personal_nummer   => 12487,
                           geb_tag           => "1970-01-01",
                           gehalt            => 3454,
                           abteilung         => "9e",
                           schulungen        => [],
                           },
   
   );


use Data::Dumper;

print Dumper(\%personen);


$personen{"vorname name"} = {
                           personal_nummer   => 12999,
                           geb_tag           => "1970-01-01",
                           gehalt            => 3454,
                           abteilung         => "9e",
                           schulungen        => [],
                           };


push @{ $personen{"vorname name"}{schulungen} }, "perl";



print Dumper(\%personen);







