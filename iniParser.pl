#!/usr/bin/env perl
use strict; use warnings;

package IniParser;
    sub new() {
        my $type = shift;
        my $this = {};
        $this->{'iniFile'} = shift;
        $this->{'err'} = "";
        $this->{'val'} = {};
        open CONFIG,"$this->{'iniFile'}" or $this->{'err'} = "open $this->{'iniFile'}: $!";
        if (! $this->{'err'}){
            my $session;
            while (my $string = <CONFIG>){
                chomp $string;
                if ( $string =~ /^#/){next;}
                if ( $string =~ /^\[(\w+)\]/ ){
                    $session = $1;
                    $this->{'val'}{$session} = {};
                }elsif($session and $string =~ /^(\w+)=(.*)/){
                    $this->{'val'}{$session}{$1} = $2;
                }
            }
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
        if (exists $this->{'val'}{$session}{$key}){
            return $this->{'val'}{$session}{$key};
        }else{
            return "";
        }
    }
1;

my $iniFile=$ARGV[0];
my $session=$ARGV[1];
my $key=$ARGV[2];

my $conf = IniParser->new($iniFile);
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
