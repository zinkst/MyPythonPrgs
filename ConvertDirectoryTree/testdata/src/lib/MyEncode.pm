package MyEncode;                                  # Namensraum definieren

use base qw(Exporter);                             # Erbe Funktionalität vom Exporter

our @EXPORT = qw(encode decode);                   # liste alle per Default exportierten Symbole

use Carp;

sub encode                                         # Kodierungs-Funktion hat einen Parameter
   {
   carp "Bitte nur 1 Parameter uebergeben" unless @_ == 1;
   return pack('u', shift);                        # Codiert und gibt das Ergebnis gleich zurueckden: 
                                                   # uebergebenen String (erster Parameter)
   }

sub decode ($)                                     # Dekodierungs-Funktion bekommt einen Parameter
   {
   return unpack('u', $_[0]);                      # dekodiert und gibt es zurueck
   }

   

return 1;



