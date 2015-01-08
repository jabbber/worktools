/*
Proxy auto-config script
author: Jabber Zhou
contact: mayjabber@gmail.com
*/
var index_Proxy = "DIRECT;";
var SSL_Proxy = "SOCKS5 127.0.0.1:1080; SOCKS5 127.0.0.1:10000;";
var base_Proxy = "PROXY 127.0.0.1:8118;";

var host_list = heredoc(function(){/*
twitter.com
*/});
host_list = host_list.split("\n");

var url_list = heredoc(function(){/*
http://ipaddress.com/
https://www.google.com/search?
http://www.google.com/url?
*/});
url_list = url_list.split("\n");

var regexp_list = heredoc(function(){/*
.+facebook\.com.*
*/});
regexp_list = regexp_list.split("\n");

function heredoc(fn) {
    return fn.toString().split('\n').slice(1,-1).join('\n') + '\n'
}

function listmatch(value,list) {
    for (var n in list)
    {
        if (list[n] !== '')
        {
            if (value.indexOf(list[n]) !== -1) return true;
        }
    }
    return false;
}

function regmatch(value) {
    for (var n in regexp_list)
    {
        if (regexp_list[n] !== '')
        {
            try {
                re = new RegExp(regexp_list[n]);
                if (re.test(value)) {return true;}
            } catch(e){continue;}
        }
    }
    return false;
}

function FindProxyForURL(url, host)
{
    if (listmatch(host,host_list)) {return SSL_Proxy;}
    if (listmatch(url,url_list)) {return SSL_Proxy;}
    if (regmatch(url)) {return SSL_Proxy;}

    return index_Proxy;
}

