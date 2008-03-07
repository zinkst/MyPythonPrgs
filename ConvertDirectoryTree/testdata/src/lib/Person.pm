package Person;

use strict;
use warnings;


use Carp qw(carp croak);

use 5.010;


sub new
   {
   my ($class, $name, $geburtstag, $geschlecht) = @_;
   
   # Ueberpruefung der Parameter, entweder via Anzahl oder bei der Zuweisung
   # Hier: Anzahl
   
   carp "Falsche Anzahl an Parametern. Aufruf: Person->new(<name>, <geburtstag>, <geschlecht>);" 
      unless @_ == 4;
   
   
   my $self =                                      # Instanzvariablen belegen.
      {
      name        => $name       // croak "Kein Name angegeben!",        # /
      geburtstag  => $geburtstag // croak "Kein Geburtstag angegeben",   # /  
      geschlecht  => $geschlecht // croak "Kein Geschlecht angeegben!",  # /
      };
   
   bless $self, $class;                            # Unser Objekt segnen (und damit erst zu einem Objekt machen)
   
   
   return $self;                                   # Rueckgabe vom Objekt
   
   }



sub name
   {
   my $self = shift;
   return $self->{name};
   }

sub geburtstag
   {
   my $self = shift;
   return $self->{geburtstag};
   }

sub geschlecht
   {
   my $self = shift;
   return $self->{geschlecht};
   }


sub test
   {
   my $self = shift;
   my $test = $self->{test};
   return $test;
   }


#
#use Date::Calc qw(Delta_YMD);
#
#sub get_age
#   {
#   my $self = shift;
#   my @now = localtime();
#   my ($y, $m, $d) = Delta_YMD(split(/-/, $self->geburtstag), $now[5]+1900, $now[4], $now[3]);
#   
#   return wantarray ? ($y, $m, $d) : $y;
#   
#   }

1;

