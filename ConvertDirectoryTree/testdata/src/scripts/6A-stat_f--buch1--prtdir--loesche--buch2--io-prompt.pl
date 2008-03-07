#!/usr/bin/perl

use warnings;
use strict;
use diagnostics;

use IO::Prompt;


my $lastokfile = "/etc/services";                  # hier schummel ich: als Default-Datei wird schon eine ausgewaehlt,
                                                   # so dass ich mir die Eingabe im erten Teil sparen kann ...
FILE_LOOP:
while (1)
   {
   my $file = prompt("Sag mir mal einen Dateinamen (* oder <leer> = Ende): ");
   
   last FILE_LOOP if $file eq "" or $file eq "*";            # Abbruch, wenn keine Eingabe (nur Return) oder wenn "*" eingegeben wurde
   
   if(-f $file)
      {
      print "Datei '$file' ist vorhanden und hat die Laenge: " . (-s $file) . " Bytes\n";
      $lastokfile = $file;
      }
   else
      {
      print "Datei '$file' existiert nicht!\n";
      }
   
   }


# =================================================


print "\n\nDie Datei '$lastokfile' hat den Inhalt:\n\n";
open (my $FILE, '<', $lastokfile) or die "Die Datei existiert nicht mehr oder anderer Fehler: $!\n";

# Variante 1:

while (my $line = <$FILE>)
   {
   print "Zeile: $line";
   }


# Variante 2: While nur in einer Zeile

print "Zeile: $_" while <$FILE>;


# Variante 3: in Array einlesen

my @content = <$FILE>;
print @content;



# Version 4: Langfassung mit Array

my $linenum = 1;
foreach (@content)
   {
   print "Zeile $linenum: $_";
   $linenum++;
   }



# die ganz kurze Variante 5:

print <$FILE>;


close $FILE;


# Variante 6,

use File::Slurp;
# use Perl6::Slurp;

print slurp($lastokfile);


my $dateiinhalt = slurp($lastokfile);
print $dateiinhalt;


# =================================================

my $dir = prompt "\n\nSag mir nun einen Verzeichnisnamen: ";

if (-d $dir)
   {
   print "Das Verzeichnis enthaelt die folgenden Dateien: \n";
   opendir (DIR, $dir) or die "Fehler beim Verzeichnis lesen: $!";
   print "  $dir/$_\n" foreach readdir(DIR);
   closedir DIR;
   }
else
   {
   print "Dieses Verzeichnis gibts nicht!\n";
   }

print "\n\n";

# ==================================================

print "Lege nun 'testdir' und ein paar Dateien an.\n";

mkdir "testdir";
chdir "testdir";

open ($FILE, '>', 'test1.alt') or die "Fehler beim Schreiben: $!\n";
print $FILE "Blabla 1\n";
close $FILE;

open ($FILE, '>', 'test2.alt') or die "Fehler beim Schreiben: $!\n";
print $FILE "Blabla 2\n";
close $FILE;

open ($FILE, '>', 'test2.neu') or die "Fehler beim Schreiben: $!\n";
print $FILE "Blabla 3\n";
close $FILE;


# ==================================================

my @loeschfiles = glob("*.alt");

foreach my $loesche (@loeschfiles)
   {
      
   my $antwort = prompt("Loesche '$loesche'? (j/n) ");
   
   if ($antwort eq "j")
      {
      print "OK, loesche $loesche...\n";
      unlink $loesche or print "Fehler beim Loeschen: $!";
      }
   }



# ===================================================

open ($FILE, $lastokfile) or die "Die Datei existiert nicht mehr oder anderer Fehler: $!\n";
my @sorted = sort <$FILE>;
close $FILE;

open (my $SORTED, '>', 'tmp/sorted.txt') or die "Kann Sortiertes File nicht zum Schreiben oeffnen: $!";
print $SORTED @sorted;
close $SORTED;


# Kurzversion:

open ($FILE, $lastokfile) or die "Die Datei existiert nicht mehr oder anderer Fehler: $!\n";
open ($SORTED, ">/tmp/sorted.txt") or die "Kann Sortiertes File nicht zum Schreiben oeffnen: $!";

print $SORTED sort <$FILE>;

close $SORTED;
close $FILE;


# Oder via Buildins:

print sort <>;




