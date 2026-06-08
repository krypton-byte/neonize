#ifndef CSTRUCT_H
#define CSTRUCT_H

#include <stdbool.h>
#include <stddef.h>

struct BytesReturn{
    char* data;
    size_t size;
};

struct ProxySettings {
    char* proxyAddress;
    bool noWebsocket;
    bool onlyLogin;
    bool noMedia;
};

#endif