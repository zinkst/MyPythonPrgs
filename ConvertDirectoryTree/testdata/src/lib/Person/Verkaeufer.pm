package Person::Verkaeufer;

use warnings;
use strict;

use base qw(Person);


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


=cut


=head2 ->new



  my $v = Person::Verkaeufer->new
     (
     name         => "Hans Wurst", 
     geburtstag   => "2000-01-01",
     gehalt       => 10000,
     geschlecht   => "m",
     );


=cut


sub new
   {
   my $class = shift;
   
   my %params = 
      (
      gehalt   => 1000,
      name     => "unbekannter Verkaeufer",
      @_,
      );
   
   my $self = $class->SUPER::new2(%params);
   
   bless $self, $class;
      
   return $self;
   
   }




=head2 gehalt

setzt das Gehalt eines Kunden oder gibt es zurück

=cut

sub gehalt
   {
   
   my $self = shift;
   if (@_)
      {
      $self->{gehalt} = $_[0];
      }
   
   return $self->{gehalt};
   
   }



=head1 AUTHOR

Alvar Freude, C<< <alvar at a-blast.org> >>

=head1 BUGS

keine bekannt

=cut

1; # End of Perlkurs::Beispiel
