#!/usr/bin/perl 

use strict;                                        # erzwinge Variablendeklaration
use warnings;                                      # schalte Warnungen an


sub test
   {
   return;
   }


sub test2 ($)
   {
   return;
   }
   
 
sub test3 ($$)
   {
   return;
   }
   
my @a = qw(skfh sdh sfash);

test();

test2(@a, @a);

test3(@a);


   
   