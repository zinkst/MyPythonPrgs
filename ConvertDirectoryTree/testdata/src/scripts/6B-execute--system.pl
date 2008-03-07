#!/usr/bin/perl 

use warnings;
use strict;
use diagnostics;



print qx(ps aux);                                  # gibt direkt alles aus

my @ps_ausgabe = qx(ps aux);                       # andere variante: lese alles in array
print @ps_ausgabe;                                 # gebe das array aus

foreach my $line (@ps_ausgabe)                     # Oder, andere Variante:
   {                                               # manuell via foreach alle Zeilen bearbeiten
   print $line;
   }



# === execute2 =====================

#
# Zuerst Langversion, 
# bearbeitet alle Zeilen mit einer While-Schleife
# Da koennte man natuerlich auch noch weitere Sachen machen,
# z.B. mit Regex filtern
#

open (PS, "ps aux|") or die "kann ps nicht starten: $!";

while (my $line = <PS>)
   {
   print $line;
   }
 
close PS;


#
# Kurze Variante, mit Direktausgabe
#

open (PS, "ps aux|") or die "kann ps nicht starten: $!";
print <PS>;
close PS;



# === system =======================

use IO::Prompt;

my $cmd = prompt("Welches Kommando möchten Sie starten? ");

system ($cmd) ;


my $status = system prompt("Und noch eins bitte! ");


if ($status)
   {
   print "Da ging was schief! $status\n"
   }
else
   {
   print "Alles OK!\n";
   }







