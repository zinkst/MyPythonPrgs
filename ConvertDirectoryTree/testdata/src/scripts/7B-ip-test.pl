#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use IO::Prompt;


# Lösung laut Musterlösung:

# Einzelnes Tupel:   (\d{1,3})
#
# my @ip_parts = /(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/;
# my @ip_parts = /(?:(\d{1,3})[.]){3}(\d{1,3})/;
# 
# ....
# if ($1 >=0 and $1 <=255 and $2 >=0 and $2 <= 255 ) ...
#
# array; ist sowieso mind 0 beim test
# 
#

#use re qw(debug);

my $text = "123.123.123.123";


if (my ($ip1, $ip2, $ip3, $ip4) = 
       $text =~ m{
          \A\s*          # Beginnt mit vielleicht ein paar Whitzespace
          (\d{1,3})\.    # Matche ein Tupel 0, 1, 123, 255, ...
          (\d{1,3})\.    # mehrfach
          (\d{1,3})\.
          (\d{1,3})
          \s*\z          # endet mit vielleicht ein paar whitespace
          }msx)
   {
   print "gefunden ...";
   }
else
   {
   print "nix da\n";
   }


__END__;

#
# Lösung nur mit Regex:
#



while (1)
   {
   
   my $ip = prompt "sag mal ne IP adresse, oder etwas mit IP-Adresse: ";
      
   if ($ip =~ 
       m{\b
         (                                         # Beginn der IP
         (?:                                       # Erste Zahl / Varianten nicht einfangen
            [01]?\d?\d                             # 0-9, 00-99, 100-199, 001-099 usw
            |                                      # ODER
            2[0-4]\d                               # 200-249
            |                                      # ODER
            25[0-5]                                # 250-255
         )
         \.
         (?:
            [01]?\d?\d
            |
            2[0-4]\d
            |
            25[0-5]
         )
         \.
         (?:
            [01]?\d?\d
            |
            2[0-4]\d
            |
            25[0-5]
         )
         \.
         (?:
            [01]?\d?\d
            |
            2[0-4]\d
            |
            25[0-5]
         )
         )
        \b
       }x)
      {
      print "OK, '$1' ist eine echte IP-Adresse!\n";
      }
   else
      {
      print "noe, ist keine IP-Adresse dabei!\n";
      }
   }





# ======================================================================================

# === nun das Dummy 7C



# ======================================================================================


# Test ###


my $zeile = "Hanswurst  123 0.0 2.3 1 S 5 18:12 /usr/local/bin/bla -x -y datei.txt";


print "$zeile\n";

# username        123   ......   18:12      /bin/bla   -x -y -z 
#  (\w+)    \s+  (\d+)   .*?    (\d\d:\d\d) 

#        (1)      (2)             (3)         (4)       (5)
  my ($username, $pid,          $uhrzeit,    $file, $parameter) = 
      $zeile =~ m
         (
         ^                                         # Begin
         (\w+)                                     # (1): Username
         \s+                                       #      Zwischenraum
         (\d+)                                     # (2): pid: Nur zahlen
         .*?                                       #      ueberspringe alles bis zum naechsten, der Uhrzeit
         (\d{2}:\d{2})                             # (3): Uhrzeit
         \s+                                       #      Zwischenraum, nicht eifangend
         (.*?)                                     # (4): file/Kommando: beliebige Zeichen, non-greedy
         \s+                                       #      Zwoischenraum zwischen kommando und params
         (.*)                                      # (5): Parameter: der ganze Rest
         )x;
 
print qq{
Username: $username     $1
pid:      $pid          $2
Uhrzeit:  $uhrzeit      $3
File:     $file         $4 
Params:   $parameter    $5

};

    (my $neu = $zeile) =~ s
         (
         ^                                         # Begin
         (\w+)                                     # (1): Username
         \s+                                       #      Zwischenraum
         (\d+)                                     # (2): pid: Nur zahlen
         .*?                                       #      ueberspringe alles bis zum naechsten, der Uhrzeit
         (\d{2}:\d{2})                             # (3): Uhrzeit
         \s+                                       #      Zwischenraum, nicht eifangend
         (.*?)                                     # (4): file/Kommando: beliebige Zeichen, non-greedy
         \s+                                       #      Zwoischenraum zwischen kommando und params
         (.*)                                      # (5): Parameter: der ganze Rest
         )
         ($1 $2 $3 $4 $5)gx;


print "ALT: $zeile\n";
print "NEU: $neu\n";



print "\n\n";






