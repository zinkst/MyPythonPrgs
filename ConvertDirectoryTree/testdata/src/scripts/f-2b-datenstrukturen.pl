#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


my $klasse2_ref = 
   {
   fritzchen =>
      {
      
      },
   };



my @noten = (1, 3, 5, 2, 3);

my $noten_test = [2.3, 3,   1, 2, 5];



my %klasse = 
   (
   fritzchen => 
      {
      geburtstag  => "1970-01-01",
      noten       => 
                     {
                     bio         => [2.3, 3,   1, 2, 5],
#                    bio         => $noten_test,
                     mathe       => [1.7, 2,   3, 4, 5],
                     englisch    => [5.1, 1.2, 3, 4, 5],
                     deutsch     => [1,   2,   5, 3, 2],
                     informatik  => [1, 1, 1],
#                     englisch    => \@noten,
#                     deutsch     => \@noten,
#                     informatik  => \@noten,

                     },
      },
   
   hutzelhugo     =>
      { 
      geburtstag  => "1970-01-01",
      noten       => 
                     {
                     bio         => [1.7, 2,   3, 4, 5],
#                    bio         => $noten_test,
                     mathe       => [2.3, 3,   1, 2, 5],
                     englisch    => [1,   2,   5, 3, 2],
                     deutsch     => [5.1, 1.2, 3, 4, 5],
                     },
      },
   
   kleintrude     => 
      {
      geburtstag  => "2008-01-01",
      noten       => 
                     {
                     bio         => [],
                     mathe       => [],
                     englisch    => [],
                     deutsch     => [],
                     physik      => [],
                     },
      },
   );



use Data::Dumper;

print Dumper(\%klasse);






my @fritzchens_bio_noten = get_marks("fritzchen", "bio");


print "Bio Noten vom Fritzchen:          ", join(", ", get_marks     ("fritzchen", "bio")), "\n";
print "Bio Noten vom Fritzchen (fast):   ", join(", ", get_marks_fast("fritzchen", "bio")), "\n";

my $noten_ref =  get_marks_sauber("hansi", "bio");
if ($noten_ref)
   {
   print "Bio Noten vom Hansi (fast):   ", join(",", @$noten_ref), "\n";
   }
else
   {
   print "Keine Noten fuer Hansi!\n";
   }


sleep 2;

set_marks("fritzchen", "bio", 6);
print "Neue Bio Noten vom Fritzchen:          ", join(", ", get_marks     ("fritzchen", "bio") ), "\n";

set_marks_fast("fritzchen", "bio", 1);
print "Neue Bio Noten vom Fritzchen:          ", join(", ", get_marks     ("fritzchen", "bio") ), "\n";

set_marks_fast("fritzchen", "bio", 1);
print "Neue Bio Noten vom Fritzchen:          ", join(", ", get_marks     ("fritzchen", "bio") ), "\n";


sub get_marks
   {
   my ($name, $fach) = @_;
   my $noten_ref = $klasse{$name}{noten}{$fach};
   return @$noten_ref;
   }

sub get_marks_fast
   {
   @{ $klasse{$_[0]}{noten}{$_[1]} };
   }

#
# Unnötig, da undef sowieso zurückgegeben wird, wenn 
# ein Teil in der Datenstruktur nicht existiert!
#
sub get_marks_sauber
   {
   my ($name, $fach) = @_;
   return unless $klasse{name};              # Fehlerabfrage: existiert der schueler?
   my $noten_ref = $klasse{$name}{noten}{$fach};
   return $noten_ref;
   }


sub set_marks
   {
   my ($name, $fach, @noten) = @_;
   my $noten_ref = $klasse{$name}{noten}{$fach};
   push @$noten_ref, @noten;
   #push @{ $klasse{$name}{noten}{$fach} }, @noten;
   }

sub set_marks_fast
   {
   push @{ $klasse{shift()}{noten}{shift()} }, @_;
   }







# =========================================




foreach my $kind (keys %klasse)
   { 
   my %eltern = 
      (
      mutter => 
         {
         name     => "Mutter von $kind",
         adresse  => "irgendwo",
         },
      vater => 
         {
         name     => "Vater von $kind",
         adresse  => "irgendwo",
         },
      );
   $klasse{$kind}{eltern} = \%eltern;
   }


print Dumper(\%klasse);






   