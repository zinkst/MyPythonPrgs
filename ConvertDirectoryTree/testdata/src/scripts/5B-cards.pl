#!/usr/bin/perl

use warnings;
use strict;
#use diagnostics;

use 5.010;

=head1 SYNOPSIS

  ./5B-cards.pl [...]
  
  -v, --verbose:      zeige Debug-Infos an
  -h, --help:         gebe eine kurze Hilfe aus
  -m, --man:          zeige Dokumentation
  -d n, --durchgaenge=n:  Anzahl der Misch-Vorgaenge
  -k n, --kartenstapel=n: Anzahl der Kartenstapel (mit 32 Karten)



=head1 DESCRIPTION

Dieses kleine Programm mischt ein paar Karten beliebig oft. 

Und damit es sich lohnt, sollte hier eine laengere Erklaerung stehen. 
Daher steht hier Blindtext. Der ist von Natur aus blind. Bla Bla bla.
Blablablabla! Bla. Blabla. Bla bla Blala. Blalala. Blablablubb. Bla Bla bla.
Bla Blubb bla. Blablablabla! Bla. Blabla. Bla bla Blala. Blalala. 
Blablablubb. Bla Bla bla. Blablablabla! Bla. Blabla. Bla bla 
Blala. Blalala. Blablablubb. Bla. Blabla. Bla bla Blala. Blalala. 
Blablablubb. Bla Bla bla. Bla Blubb bla. Blablablabla! Bla. Blabla. 
Bla bla Blala. Blalala. Blablablubb. Bla Bla bla. Blablablabla! Bla. 
Blabla. Bla bla Blala. Blalala. Blablablubb



=cut




use Time::HiRes qw(time);                          # Zeitmessung Nanosekundengenau


use Getopt::Long;                                  # Behandlung von Eingabeparameter
use Pod::Usage;                                    # Funktionen zum Ausgeben der Dokumentation



my ($help, $man, $debug);
my ($mischen, $kartenstapel) = (32, 1);
GetOptions
   (
   'help|?'           => \$help,
   'man'              => \$man,
   'verbose!'         => \$debug,
   'durchgaenge=i'    => \$mischen,
   'kartenstapel=i'   => \$kartenstapel, 
   ) or pod2usage(2);


# Gebe Hilfe aus wenn gewuenscht

pod2usage(1) if $help;
pod2usage(-exitstatus => 0, -verbose => 2) if $man;


#
# Wenn keine Hilfe gewünscht oder keine falschen Parameter
# dann geht es hier los!
#

say "Habe $kartenstapel Kartenstabel mit je 32 Karten und mische $mischen mal";


#
# Kartenstapel erzeugen
# Ich bin faul und lasse es den Computer machen!
#

# Liste aller Kartentypen

my @typ = (7..10, qw(Bube Dame Koenig Ass));


# Oder, länger:

#my @typ = qw(
#   7
#   8 
#   9 
#   10
#   bube
#   dame
#   Koenig
#   Ass
#   );



# Leere Karten erzeugen

my (@karten_karo, @karten_herz, @karten_pik, @karten_kreuz);

#push @karten_karo,  "Karo $_"  foreach @typ;       # Generiert die einzelnen Kartenbezeichnungen
#push @karten_herz,  "Herz $_"  foreach @typ;       #  ... ist Weniger Tipparbeit und flexibler!
#push @karten_pik,   "Pik $_"   foreach @typ;
#push @karten_kreuz, "Kreuz $_" foreach @typ;


foreach my $kartentyp (@typ)
   {
   push @karten_karo,  "Karo $kartentyp";
   push @karten_herz,  "Herz $kartentyp";
   push @karten_pik,   "Pik $kartentyp";
   push @karten_kreuz, "Kreuz $kartentyp";
   }


# Und die ganzen Karten werden nun einem ganzen Kartenstapel zugewiesen
my @karten;
push @karten, @karten_karo, @karten_herz, @karten_pik, @karten_kreuz
   for (1..$kartenstapel);

use Data::Dumper;
print Dumper
   (
   {
   typ         => \@typ,
   karo        => \@karten_karo,
   herz        => \@karten_herz,
   pik         => \@karten_pik,
   kreuz       => \@karten_kreuz,
   alle_karten => \@karten,
   }
   ) if $debug;


#exit;


#
# Karten Mischen
#

my $starttime = time;


=begin variante 1

# diese oder die Kurzvariante wegkommentieren

for (1..$mischen)
   {
   my $einfuegeposition = int(rand(scalar @karten));
   my $erste_karte      = shift @karten;
   splice (@karten, $einfuegeposition, 0, $erste_karte);
   }

=end

=cut


# Kurzvariante:
splice (@karten, int(rand(@karten)), 0, shift @karten) for 1..$mischen;



my $endtime = time;


print Dumper(\@karten) if $debug;




#
# Karten auf die Spieler verteilen
#

my (@spieler1, @spieler2, @spieler3, @spieler4);

for (1..4)
   {
   push @spieler1, shift @karten, shift @karten;
   # push @spieler1, splice(@karten, 0, 2);
   push @spieler2, splice(@karten, 0, 2);
   push @spieler3, splice(@karten, 0, 2);
   push @spieler4, splice(@karten, 0, 2);
   }


#
# ausgabe
#

print Dumper
   ({
   spieler_1 => \@spieler1,
   spieler_2 => \@spieler2,
   spieler_3 => \@spieler3,
   spieler_4 => \@spieler4,
   }) if $debug;


print qq{
Die Spieler haben nun die folgenden Karten:
===========================================

    Spieler 1    | Spieler 2    | Spieler 3    | Spieler 4  
   --------------+--------------+--------------+--------------
};

for my $index (0..$#spieler1)
   {
   printf "    %-12s | %-12s | %-12s | %-12s \n", 
      $spieler1[$index], 
      $spieler2[$index], 
      $spieler3[$index], 
      $spieler4[$index]; 
   }



print "\nBenoetigte Zeit zum Mischen: " . ($endtime - $starttime) . " Sekunden\n";

my $alle_pro_sek = 1/($endtime - $starttime);
printf "Mische %.2f Karten pro Sekunde, also alle Karten %.2f mal pro Sekunde\n\n", $alle_pro_sek*$mischen, $alle_pro_sek;




__END__

