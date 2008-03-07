#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use IO::Prompt;


=begin weg
# test für 3:

while (1)
   {
   my $text = prompt("Sag noch mal was: ");
   
   print "Muster passt" . ( $text =~ /^ *[0-9]+ *$/ ? "" : " nicht" ) . ".\n";
   }


exit;

=end

=cut


#
# Aufgabe 1:
#
# Regex: \b[pP]erl\b 
#

my $text = prompt("Sag mal was: ");

if ($text =~ /\b[pP]erl\b/)
   {
   print "Das Wort Perl ist vorhanden!\n";
   }
else
   {
   print "Schade, schade, das Wort ist nicht vorhanden!\n";
   }


#
# Andere Variante:
#

print "Wort ist " . ( $text =~ /\bperl\b/i ? "" : "nicht " ) . "vorhanden.\n";
print "Wort ist " . ( $text !~ /\bperl\b/i ? "nicht " : "" ) . "vorhanden.\n";



#
# Aufgabe 2:
#
# Regex: \b[wW]ah?l\b
#

$text = prompt("Sag noch mal was: ");

print "Wort ist " . ( $text =~ /\b[Ww]ah?l\b/ ? "" : "nicht " ) . "vorhanden.\n";



#
# Aufgabe 3:
# 
# Regex: ^[ ]*[0-9]+[ ]*$
# Regex: ^\s*\d+\s*$               
# # \A \z
#

$text = prompt("Sag noch mal was: ");

print "Muster passt" . ( $text =~ /^ *[0-9]+ *$/ ? "" : " nicht" ) . ".\n";





