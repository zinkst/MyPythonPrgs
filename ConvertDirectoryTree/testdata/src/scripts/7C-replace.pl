#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

my $suche = shift;
my $ersetze = shift;

defined $suche and defined $ersetze or die "Benutzung: $0 such_muster ersetzungs_text [dateinamen]";


while (<>)
   {
   s/$suche/$ersetze/igo;
   print;
   }


