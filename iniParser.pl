#!/usr/bin/env perl
use strict; use warnings;

my $session=$ARGV[0];
my $key=$ARGV[1];

package IniParser;
    sub new() {
        my $type = shift;
        my $this = {};
        $this->{'iniFile'} = shift;
        $this->{'err'} = "";
        open CONFIG,"$this->{'iniFile'}" or $this->{'err'} = "open $this->{'iniFile'}: $!";
        if (! $this->{'err'}){
            close CONFIG;
        }
        bless $this, $type;
        return $this;
    }

    sub val()
    {
        my $this = shift @_;
        my $session = shift;
        my $key = shift;
        my $flag = 0;
        open CONFIG,"$this->{'iniFile'}" or $this->{'err'} = "open $this->{'iniFile'}: $!";
        if (! $this->{'err'}){
            while (my $string = <CONFIG>){
                chomp $string;
                if($flag == 0){
                    if ( $string =~ /^\[$session\]/ ){
                    $flag = 1;
                    }
                }else{
                    if( $string =~ /^\[/){
                    last;}
                    if ( $string =~ /^#/){
                        next;
                    }
                    if ($string =~ /^(\w+)=(.*)/){
                        my $k = $1;
                        my $v = $2;
                        if($k eq $key){
                            return $v;
                        }
                    }
                }
            }
            close CONFIG;
        }
        return "";
    }
1;

my $conf = IniParser->new("config.ini");
if ($conf->{'err'}){
    print $conf->{'err'};
    print "\n";
    exit 1;
}
if ($conf->val($session, $key)){
    print "I find [$session] $key 's value ". $conf->val($session, $key) .".\n";
}else{
    print "I can not find [$session] $key 's value.\n";
}
