/*
Proxy auto-config script
author: Jabber Zhou
contact: mayjabber#gmail.com
*/
var index_Proxy = "DIRECT;";
var SSL_Proxy = "SOCKS5 127.0.0.1:1080; SOCKS5 127.0.0.1:10000;";
var base_Proxy = "PROXY 127.0.0.1:8118;";

var domain_list = heredoc(function(){/*
twitter.com
youtube.com
ytimg.com
*/});

var url_list = heredoc(function(){/*
http://ipaddress.com/
https://www.google.com/search?
http://www.google.com/url?
*/});

var regexp_list = heredoc(function(){/*
.+facebook\.com.*
https?://www.google.com.*
*/});


domain_list = domain_list.split("\n");
var domain_object = {};
for (var n in domain_list) {
    if (domain_list[n] !== '') {
        domain_object[domain_list[n]] = true;
    }
};

url_list = url_list.split("\n");
regexp_list = regexp_list.split("\n");

function heredoc(fn) {
    return fn.toString().split('\n').slice(1,-1).join('\n') + '\n'
}

var hasOwnProperty = Object.hasOwnProperty;
function domainMatch(host) {
    var suffix;
    var pos = host.lastIndexOf('.');
    pos = host.lastIndexOf('.', pos - 1);
    while(1) {
        if (pos <= 0) {
            if (hasOwnProperty.call(domain_object, host)) {
                return true;
            } else {
                return false;
            }
        }
        suffix = host.substring(pos + 1);
        if (hasOwnProperty.call(domain_object, suffix)) {
            return true;
        }
        pos = host.lastIndexOf('.', pos - 1);
    }
}

function urlMatch(url) {
    for (var n in url_list){
        if (url_list[n] !== ''){
            if (url.indexOf(url_list[n]) !== -1) return true;
        }
    }
    return false;
}

function regMatch(url) {
    for (var n in regexp_list){
        if (regexp_list[n] !== ''){
            try {
                re = new RegExp(regexp_list[n]);
                if (re.test(url)) {return true;}
            } catch(e){continue;}
        }
    }
    return false;
}

function FindProxyForURL(url, host)
{
    if (domainMatch(host)) {return SSL_Proxy;}
    if (urlMatch(url)) {return SSL_Proxy;}
    if (regMatch(url)) {return SSL_Proxy;}

    return index_Proxy;
}

