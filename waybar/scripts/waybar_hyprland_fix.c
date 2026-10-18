#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/uio.h>

static ssize_t (*real_write)(int fd, const void *buf, size_t count) = NULL;
static ssize_t (*real_send)(int sockfd, const void *buf, size_t len, int flags) = NULL;
static ssize_t (*real_sendto)(int sockfd, const void *buf, size_t len, int flags,
                              const struct sockaddr *dest_addr, socklen_t addrlen) = NULL;

static void init_hooks(void) {
    if (!real_write) real_write = (ssize_t (*)(int, const void *, size_t))dlsym(RTLD_NEXT, "write");
    if (!real_send)  real_send  = (ssize_t (*)(int, const void *, size_t, int))dlsym(RTLD_NEXT, "send");
    if (!real_sendto) real_sendto = (ssize_t (*)(int, const void *, size_t, int, const struct sockaddr *, socklen_t))dlsym(RTLD_NEXT, "sendto");
}

static int rewrite_dispatch(const char *buf, size_t len, char *out, size_t out_max) {
    if (!buf || len == 0) return 0;

    // Optional leading slash
    const char *p = buf;
    size_t rem = len;
    if (rem > 0 && *p == '/') {
        p++;
        rem--;
    }

    char arg[128] = {0};

    // 1. "dispatch workspace "
    static const char pfx_ws[] = "dispatch workspace ";
    size_t pfx_ws_len = sizeof(pfx_ws) - 1;
    if (rem >= pfx_ws_len && memcmp(p, pfx_ws, pfx_ws_len) == 0) {
        size_t arglen = rem - pfx_ws_len;
        if (arglen >= sizeof(arg)) arglen = sizeof(arg) - 1;
        memcpy(arg, p + pfx_ws_len, arglen);
        arg[arglen] = '\0';
        while (arglen > 0 && (arg[arglen - 1] == '\r' || arg[arglen - 1] == '\n' || arg[arglen - 1] == ' ')) {
            arg[--arglen] = '\0';
        }
        snprintf(out, out_max, "/dispatch hl.dsp.focus({ workspace = \"%s\" })", arg);
        return 1;
    }

    // 2. "dispatch focusworkspaceoncurrentmonitor "
    static const char pfx_foc[] = "dispatch focusworkspaceoncurrentmonitor ";
    size_t pfx_foc_len = sizeof(pfx_foc) - 1;
    if (rem >= pfx_foc_len && memcmp(p, pfx_foc, pfx_foc_len) == 0) {
        size_t arglen = rem - pfx_foc_len;
        if (arglen >= sizeof(arg)) arglen = sizeof(arg) - 1;
        memcpy(arg, p + pfx_foc_len, arglen);
        arg[arglen] = '\0';
        while (arglen > 0 && (arg[arglen - 1] == '\r' || arg[arglen - 1] == '\n' || arg[arglen - 1] == ' ')) {
            arg[--arglen] = '\0';
        }
        snprintf(out, out_max, "/dispatch hl.dsp.focus({ workspace = \"%s\", monitor = \"current\" })", arg);
        return 1;
    }

    // 3. "dispatch togglespecialworkspace"
    static const char pfx_sp[] = "dispatch togglespecialworkspace";
    size_t pfx_sp_len = sizeof(pfx_sp) - 1;
    if (rem >= pfx_sp_len && memcmp(p, pfx_sp, pfx_sp_len) == 0) {
        p += pfx_sp_len;
        rem -= pfx_sp_len;
        while (rem > 0 && (*p == ' ' || *p == '\t')) {
            p++;
            rem--;
        }
        if (rem > 0) {
            size_t arglen = rem;
            if (arglen >= sizeof(arg)) arglen = sizeof(arg) - 1;
            memcpy(arg, p, arglen);
            arg[arglen] = '\0';
            while (arglen > 0 && (arg[arglen - 1] == '\r' || arg[arglen - 1] == '\n' || arg[arglen - 1] == ' ')) {
                arg[--arglen] = '\0';
            }
            snprintf(out, out_max, "/dispatch hl.dsp.workspace.toggle_special(\"%s\")", arg);
        } else {
            snprintf(out, out_max, "/dispatch hl.dsp.workspace.toggle_special()");
        }
        return 1;
    }

    return 0;
}

ssize_t write(int fd, const void *buf, size_t count) {
    init_hooks();
    if (buf && count > 0) {
        char rewritten[512];
        if (rewrite_dispatch((const char *)buf, count, rewritten, sizeof(rewritten))) {
            size_t new_len = strlen(rewritten);
            ssize_t ret = real_write(fd, rewritten, new_len);
            if (ret < 0) return ret;
            return count; // Return original count so caller loop finishes
        }
    }
    return real_write(fd, buf, count);
}

ssize_t send(int sockfd, const void *buf, size_t len, int flags) {
    init_hooks();
    if (buf && len > 0) {
        char rewritten[512];
        if (rewrite_dispatch((const char *)buf, len, rewritten, sizeof(rewritten))) {
            size_t new_len = strlen(rewritten);
            ssize_t ret = real_send(sockfd, rewritten, new_len, flags);
            if (ret < 0) return ret;
            return len;
        }
    }
    return real_send(sockfd, buf, len, flags);
}

ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
               const struct sockaddr *dest_addr, socklen_t addrlen) {
    init_hooks();
    if (buf && len > 0) {
        char rewritten[512];
        if (rewrite_dispatch((const char *)buf, len, rewritten, sizeof(rewritten))) {
            size_t new_len = strlen(rewritten);
            ssize_t ret = real_sendto(sockfd, rewritten, new_len, flags, dest_addr, addrlen);
            if (ret < 0) return ret;
            return len;
        }
    }
    return real_sendto(sockfd, buf, len, flags, dest_addr, addrlen);
}
