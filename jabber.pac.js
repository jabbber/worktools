/*
Proxy auto-config script
author: Jabber Zhou
contact: mayjabber#gmail.com
*/
var index_Proxy = "DIRECT;";
var SSL_Proxy = "SOCKS5 127.0.0.1:1080;";
var base_Proxy = "PROXY 127.0.0.1:8087;";
var work_Proxy = "SOCKS5 192.168.1.252:10001";

var https_Proxy = SSL_Proxy + base_Proxy + index_Proxy;
var http_Proxy = base_Proxy + SSL_Proxy + index_Proxy;

var domain_list = heredoc(function(){/*
twitter.com
ip138.com
ipaddress.com
*/});

var url_list = heredoc(function(){/*
https://www.google.com/search?
http://www.google.com/url?
*/});

var regexp_list = heredoc(function(){/*
.+facebook\.com.*
https?://www.google.com.*
*/});

var work_list = heredoc(function(){/*
://188\.188\..*
://192\.168\.[489(?:10)]\..*
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
work_list = work_list.split("\n");

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

function regMatch(url,list) {
    for (var n in list){
        if (list[n] !== ''){
            try {
                re = new RegExp(list[n]);
                if (re.test(url)) {return true;}
            } catch(e){continue;}
        }
    }
    return false;
}

function switchProxy(url) {
    if (url.indexOf('https://') === -1 ) {
        return http_Proxy;
    }else{
        return https_Proxy;
    }
}

function FindProxyForURL(url, host)
{
    if (regMatch(url,work_list)) {return work_Proxy;}
    if (domainMatch(host)) {return switchProxy(url);}
    if (urlMatch(url)) {return switchProxy(url);}
    if (regMatch(url,regexp_list)) {return switchProxy(url);}

    return index_Proxy;
}

