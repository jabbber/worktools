#!/usr/bin/perl
#Company: Skybility
#Powered by: zwj
#Version: 1.0.0
#Last modify: 2013-11-18

use strict;
use warnings;

sub getBondInfo {
    my($bond) = shift @_;
    my(%bond);
    if(-e $bond){
        open BOND, $bond;
        while (<BOND>) {
            chomp($_);
            if ( index($_,": ") == -1){
                next;}
            my($key, $value) = split(": ", $_);
            if (exists $bond{$key}) {
                $bond{$key} .= " ".$value;
            } else {
                $bond{$key} = $value;
            }
        }
        close BOND;
    } else{
        $bond{"Bonding Mode"} = "None";
    }
    %bond;
}

sub getIP {
    my($interface) = shift @_;
    my $request = `ip addr show $interface 2>/dev/null`;
    my $ip = "None";
    if ($request =~ /inet\s(.*?)\s/) { $ip =  $1; }
    $ip;
}

sub getSP {
    my($interface) = shift @_;
    my $request = `ethtool $interface 2>/dev/null`;
    my $sp = "Unknow";
    if ($request =~ /Supported ports:\s\[\s(\w+?)\s\]/) { $sp = $1; }
    $sp;
}

#check and output
print "Homename\tip1\tip2\tbond0 mode\tbond0 slave\tbond1 mode\tbond1 slave\tSupported ports\n";
chomp(my $hostname =  `hostname`);
print $hostname."\t";
my %bond0 = &getBondInfo("/proc/net/bonding/bond0");
my %bond1 = &getBondInfo("/proc/net/bonding/bond1");

if ($bond0{"Bonding Mode"} eq "None" and $bond1{"Bonding Mode"} eq "None"){
    print "This Server have not any bonding network."
}else{
    print &getIP("bond0")."\t";
    print &getIP("bond1")."\t";
    print $bond0{"Bonding Mode"}."\t";
    print $bond0{"Slave Interface"}."\t";
    print $bond1{"Bonding Mode"}."\t";
    print $bond1{"Slave Interface"}."\t";

    #get device
    my @netdev;
    open NETDEV, "/proc/net/dev";
    while (<NETDEV>){
        if ($_ =~ /^\s+(eth\d+)\:/){ push(@netdev, $1);}
    }
    close NETDEV;

    foreach(@netdev){
        print $_."[".&getSP($_)."] ";
    }
}
print "\t\t \t\n";
