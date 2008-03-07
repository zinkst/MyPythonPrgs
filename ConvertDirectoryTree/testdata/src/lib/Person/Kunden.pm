package Person::Kunden;

use warnings;
use strict;

=head1 NAME

Person::Kunden - Kunden-Klasse fuer Personen!

=head1 VERSION

Version 0.01

=cut

our $VERSION = '0.01';

=head1 SYNOPSIS


Perhaps a little code snippet.

    use Person::Kunden;

    my $kunde = Person::Kunden->new();
    $kunde->status(123);
    
    print "Kunde " . $kunde->name . "hat den Status " . $kunde->status . "\n";



=head1 OEFFENTLICHE METHODEN

=head2 status

setzt den Status eines Kunden oder gibt dessen Status zurück

=cut

sub status 
   {
   
   my $self = shift;
   if (@_)
      {
      $self->{status} = $_[0];
      }
   
   return $self->{status};
   
   }



=head1 AUTHOR

Alvar Freude, C<< <alvar at a-blast.org> >>

=head1 BUGS

keine bekannt

=cut

1; # End of Perlkurs::Beispiel
