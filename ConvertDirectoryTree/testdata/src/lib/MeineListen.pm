package MeineListen;


use strict;
use warnings;

use base qw(Exporter);
our @EXPORT = qw(min max);


sub min
   {
   return (sort {$a <=> $b} @_)[0];
   }

sub max
   {
   return (sort {$a <=> $b} @_)[-1];
   }


return 1;

   
