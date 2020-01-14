function i(e, t, n) {
                var a, r, i, o, s, c, l, u, b, A = 0, C = [], v = 0, E = !1, w = [], S = [], I = !1, O = !1;
                if (a = (n = n || {}).encoding || "UTF8",
                b = n.numRounds || 1,
                i = m(t, a),
                b !== parseInt(b, 10) || 1 > b)
                    throw Error("numRounds must a integer >= 1");
                if ("SHA-1" === e)
                    s = 512,
                    c = x,
                    l = H,
                    o = 160,
                    u = function(e) {
                        return e.slice()
                    }
                    ;
                else if (0 === e.lastIndexOf("SHA-", 0))
                    if (c = function(t, n) {
                        return q(t, n, e)
                    }
                    ,
                    l = function(t, n, a, r) {
                        var i, o;
                        if ("SHA-224" === e || "SHA-256" === e)
                            i = 15 + (n + 65 >>> 9 << 4),
                            o = 16;
                        else {
                            if ("SHA-384" !== e && "SHA-512" !== e)
                                throw Error("Unexpected error in SHA-2 implementation");
                            i = 31 + (n + 129 >>> 10 << 5),
                            o = 32
                        }
                        for (; t.length <= i; )
                            t.push(0);
                        for (t[n >>> 5] |= 128 << 24 - n % 32,
                        n += a,
                        t[i] = 4294967295 & n,
                        t[i - 1] = n / 4294967296 | 0,
                        a = t.length,
                        n = 0; n < a; n += o)
                            r = q(t.slice(n, n + o), r, e);
                        if ("SHA-224" === e)
                            t = [r[0], r[1], r[2], r[3], r[4], r[5], r[6]];
                        else if ("SHA-256" === e)
                            t = r;
                        else if ("SHA-384" === e)
                            t = [r[0].a, r[0].b, r[1].a, r[1].b, r[2].a, r[2].b, r[3].a, r[3].b, r[4].a, r[4].b, r[5].a, r[5].b];
                        else {
                            if ("SHA-512" !== e)
                                throw Error("Unexpected error in SHA-2 implementation");
                            t = [r[0].a, r[0].b, r[1].a, r[1].b, r[2].a, r[2].b, r[3].a, r[3].b, r[4].a, r[4].b, r[5].a, r[5].b, r[6].a, r[6].b, r[7].a, r[7].b]
                        }
                        return t
                    }
                    ,
                    u = function(e) {
                        return e.slice()
                    }
                    ,
                    "SHA-224" === e)
                        s = 512,
                        o = 224;
                    else if ("SHA-256" === e)
                        s = 512,
                        o = 256;
                    else if ("SHA-384" === e)
                        s = 1024,
                        o = 384;
                    else {
                        if ("SHA-512" !== e)
                            throw Error("Chosen SHA variant is not supported");
                        s = 1024,
                        o = 512
                    }
                else {
                    if (0 !== e.lastIndexOf("SHA3-", 0) && 0 !== e.lastIndexOf("SHAKE", 0))
                        throw Error("Chosen SHA variant is not supported");
                    var B = 6;
                    if (c = J,
                    u = function(e) {
                        var t, n = [];
                        for (t = 0; 5 > t; t += 1)
                            n[t] = e[t].slice();
                        return n
                    }
                    ,
                    "SHA3-224" === e)
                        s = 1152,
                        o = 224;
                    else if ("SHA3-256" === e)
                        s = 1088,
                        o = 256;
                    else if ("SHA3-384" === e)
                        s = 832,
                        o = 384;
                    else if ("SHA3-512" === e)
                        s = 576,
                        o = 512;
                    else if ("SHAKE128" === e)
                        s = 1344,
                        o = -1,
                        B = 31,
                        O = !0;
                    else {
                        if ("SHAKE256" !== e)
                            throw Error("Chosen SHA variant is not supported");
                        s = 1088,
                        o = -1,
                        B = 31,
                        O = !0
                    }
                    l = function(e, t, n, a, r) {
                        var i, o = B, c = [], l = (n = s) >>> 5, u = 0, d = t >>> 5;
                        for (i = 0; i < d && t >= n; i += l)
                            a = J(e.slice(i, i + l), a),
                            t -= n;
                        for (e = e.slice(i),
                        t %= n; e.length < l; )
                            e.push(0);
                        for (e[(i = t >>> 3) >> 2] ^= o << 24 - i % 4 * 8,
                        e[l - 1] ^= 128,
                        a = J(e, a); 32 * c.length < r && (e = a[u % 5][u / 5 | 0],
                        c.push((255 & e.b) << 24 | (65280 & e.b) << 8 | (16711680 & e.b) >> 8 | e.b >>> 24),
                        !(32 * c.length >= r)); )
                            c.push((255 & e.a) << 24 | (65280 & e.a) << 8 | (16711680 & e.a) >> 8 | e.a >>> 24),
                            0 == 64 * (u += 1) % n && J(null, a);
                        return c
                    }
                }
                r = z(e),
                this.setHMACKey = function(t, n, i) {
                    var u;
                    if (!0 === E)
                        throw Error("HMAC key already set");
                    if (!0 === I)
                        throw Error("Cannot set HMAC key after calling update");
                    if (!0 === O)
                        throw Error("SHAKE is not supported for HMAC");
                    if (t = (n = m(n, a = (i || {}).encoding || "UTF8")(t)).binLen,
                    n = n.value,
                    i = (u = s >>> 3) / 4 - 1,
                    u < t / 8) {
                        for (n = l(n, t, 0, z(e), o); n.length <= i; )
                            n.push(0);
                        n[i] &= 4294967040
                    } else if (u > t / 8) {
                        for (; n.length <= i; )
                            n.push(0);
                        n[i] &= 4294967040
                    }
                    for (t = 0; t <= i; t += 1)
                        w[t] = 909522486 ^ n[t],
                        S[t] = 1549556828 ^ n[t];
                    r = c(w, r),
                    A = s,
                    E = !0
                }
                ,
                this.update = function(e) {
                    var t, n, a, o = 0, l = s >>> 5;
                    for (e = (t = i(e, C, v)).binLen,
                    n = t.value,
                    t = e >>> 5,
                    a = 0; a < t; a += l)
                        o + s <= e && (r = c(n.slice(a, a + l), r),
                        o += s);
                    A += o,
                    C = n.slice(o >>> 5),
                    v = e % s,
                    I = !0
                }
                ,
                this.getHash = function(t, n) {
                    var a, i, s, c;
                    if (!0 === E)
                        throw Error("Cannot call getHash after setting HMAC key");
                    if (s = f(n),
                    !0 === O) {
                        if (-1 === s.shakeLen)
                            throw Error("shakeLen must be specified in options");
                        o = s.shakeLen
                    }
                    switch (t) {
                    case "HEX":
                        a = function(e) {
                            return d(e, o, s)
                        }
                        ;
                        break;
                    case "B64":
                        a = function(e) {
                            return h(e, o, s)
                        }
                        ;
                        break;
                    case "BYTES":
                        a = function(e) {
                            return p(e, o)
                        }
                        ;
                        break;
                    case "ARRAYBUFFER":
                        try {
                            i = new ArrayBuffer(0)
                        } catch (e) {
                            throw Error("ARRAYBUFFER not supported by this environment")
                        }
                        a = function(e) {
                            return g(e, o)
                        }
                        ;
                        break;
                    default:
                        throw Error("format must be HEX, B64, BYTES, or ARRAYBUFFER")
                    }
                    for (c = l(C.slice(), v, A, u(r), o),
                    i = 1; i < b; i += 1)
                        !0 === O && 0 != o % 32 && (c[c.length - 1] &= 4294967040 << 24 - o % 32),
                        c = l(c, o, 0, z(e), o);
                    return a(c)
                }
                ,
                this.getHMAC = function(t, n) {
                    var a, i, m, b;
                    if (!1 === E)
                        throw Error("Cannot call getHMAC without first setting HMAC key");
                    switch (m = f(n),
                    t) {
                    case "HEX":
                        a = function(e) {
                            return d(e, o, m)
                        }
                        ;
                        break;
                    case "B64":
                        a = function(e) {
                            return h(e, o, m)
                        }
                        ;
                        break;
                    case "BYTES":
                        a = function(e) {
                            return p(e, o)
                        }
                        ;
                        break;
                    case "ARRAYBUFFER":
                        try {
                            a = new ArrayBuffer(0)
                        } catch (e) {
                            throw Error("ARRAYBUFFER not supported by this environment")
                        }
                        a = function(e) {
                            return g(e, o)
                        }
                        ;
                        break;
                    default:
                        throw Error("outputFormat must be HEX, B64, BYTES, or ARRAYBUFFER")
                    }
                    return i = l(C.slice(), v, A, u(r), o),
                    b = c(S, z(e)),
                    a(b = l(i, o, s, b, o))
                }
            }
            function o(e, t) {
                this.a = e,
                this.b = t
            }
            function s(e, t, n) {
                var a, r, i, o, s, c = e.length;
                if (t = t || [0],
                s = (n = n || 0) >>> 3,
                0 != c % 2)
                    throw Error("String of HEX type must be in byte increments");
                for (a = 0; a < c; a += 2) {
                    if (r = parseInt(e.substr(a, 2), 16),
                    isNaN(r))
                        throw Error("String of HEX type contains invalid characters");
                    for (i = (o = (a >>> 1) + s) >>> 2; t.length <= i; )
                        t.push(0);
                    t[i] |= r << 8 * (3 - o % 4)
                }
                return {
                    value: t,
                    binLen: 4 * c + n
                }
            }
            function c(e, t, n) {
                var a, r, i, o, s = [];
                s = t || [0];
                for (r = (n = n || 0) >>> 3,
                a = 0; a < e.length; a += 1)
                    t = e.charCodeAt(a),
                    i = (o = a + r) >>> 2,
                    s.length <= i && s.push(0),
                    s[i] |= t << 8 * (3 - o % 4);
                return {
                    value: s,
                    binLen: 8 * e.length + n
                }
            }
            function l(e, t, n) {
                var a, r, i, o, s, c, l = [], u = 0;
                l = t || [0];
                if (t = (n = n || 0) >>> 3,
                -1 === e.search(/^[a-zA-Z0-9=+\/]+$/))
                    throw Error("Invalid character in base-64 string");
                if (r = e.indexOf("="),
                e = e.replace(/\=/g, ""),
                -1 !== r && r < e.length)
                    throw Error("Invalid '=' found in base-64 string");
                for (r = 0; r < e.length; r += 4) {
                    for (s = e.substr(r, 4),
                    i = o = 0; i < s.length; i += 1)
                        o |= (a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".indexOf(s[i])) << 18 - 6 * i;
                    for (i = 0; i < s.length - 1; i += 1) {
                        for (a = (c = u + t) >>> 2; l.length <= a; )
                            l.push(0);
                        l[a] |= (o >>> 16 - 8 * i & 255) << 8 * (3 - c % 4),
                        u += 1
                    }
                }
                return {
                    value: l,
                    binLen: 8 * u + n
                }
            }
            function u(e, t, n) {
                var a, r, i, o = [];
                o = t || [0];
                for (a = (n = n || 0) >>> 3,
                t = 0; t < e.byteLength; t += 1)
                    r = (i = t + a) >>> 2,
                    o.length <= r && o.push(0),
                    o[r] |= e[t] << 8 * (3 - i % 4);
                return {
                    value: o,
                    binLen: 8 * e.byteLength + n
                }
            }
            function d(e, t, n) {
                var a, r, i = "";
                for (t /= 8,
                a = 0; a < t; a += 1)
                    r = e[a >>> 2] >>> 8 * (3 - a % 4),
                    i += "0123456789abcdef".charAt(r >>> 4 & 15) + "0123456789abcdef".charAt(15 & r);
                return n.outputUpper ? i.toUpperCase() : i
            }
            function h(e, t, n) {
                var a, r, i, o = "", s = t / 8;
                for (a = 0; a < s; a += 3)
                    for (r = a + 1 < s ? e[a + 1 >>> 2] : 0,
                    i = a + 2 < s ? e[a + 2 >>> 2] : 0,
                    i = (e[a >>> 2] >>> 8 * (3 - a % 4) & 255) << 16 | (r >>> 8 * (3 - (a + 1) % 4) & 255) << 8 | i >>> 8 * (3 - (a + 2) % 4) & 255,
                    r = 0; 4 > r; r += 1)
                        o += 8 * a + 6 * r <= t ? "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(i >>> 6 * (3 - r) & 63) : n.b64Pad;
                return o
            }
            function p(e, t) {
                var n, a, r = "", i = t / 8;
                for (n = 0; n < i; n += 1)
                    a = e[n >>> 2] >>> 8 * (3 - n % 4) & 255,
                    r += String.fromCharCode(a);
                return r
            }
            function g(e, t) {
                var n, a = t / 8, r = new ArrayBuffer(a);
                for (n = 0; n < a; n += 1)
                    r[n] = e[n >>> 2] >>> 8 * (3 - n % 4) & 255;
                return r
            }
            function f(e) {
                var t = {
                    outputUpper: !1,
                    b64Pad: "=",
                    shakeLen: -1
                };
                if (e = e || {},
                t.outputUpper = e.outputUpper || !1,
                !0 === e.hasOwnProperty("b64Pad") && (t.b64Pad = e.b64Pad),
                !0 === e.hasOwnProperty("shakeLen")) {
                    if (0 != e.shakeLen % 8)
                        throw Error("shakeLen must be a multiple of 8");
                    t.shakeLen = e.shakeLen
                }
                if ("boolean" != typeof t.outputUpper)
                    throw Error("Invalid outputUpper formatting option");
                if ("string" != typeof t.b64Pad)
                    throw Error("Invalid b64Pad formatting option");
                return t
            }
            function m(e, t) {
                var n;
                switch (t) {
                case "UTF8":
                case "UTF16BE":
                case "UTF16LE":
                    break;
                default:
                    throw Error("encoding must be UTF8, UTF16BE, or UTF16LE")
                }
                switch (e) {
                case "HEX":
                    n = s;
                    break;
                case "TEXT":
                    n = function(e, n, a) {
                        var r, i, o, s, c, l = [], u = [], d = 0;
                        l = n || [0];
                        if (o = (n = a || 0) >>> 3,
                        "UTF8" === t)
                            for (r = 0; r < e.length; r += 1)
                                for (u = [],
                                128 > (a = e.charCodeAt(r)) ? u.push(a) : 2048 > a ? (u.push(192 | a >>> 6),
                                u.push(128 | 63 & a)) : 55296 > a || 57344 <= a ? u.push(224 | a >>> 12, 128 | a >>> 6 & 63, 128 | 63 & a) : (r += 1,
                                a = 65536 + ((1023 & a) << 10 | 1023 & e.charCodeAt(r)),
                                u.push(240 | a >>> 18, 128 | a >>> 12 & 63, 128 | a >>> 6 & 63, 128 | 63 & a)),
                                i = 0; i < u.length; i += 1) {
                                    for (s = (c = d + o) >>> 2; l.length <= s; )
                                        l.push(0);
                                    l[s] |= u[i] << 8 * (3 - c % 4),
                                    d += 1
                                }
                        else if ("UTF16BE" === t || "UTF16LE" === t)
                            for (r = 0; r < e.length; r += 1) {
                                for (a = e.charCodeAt(r),
                                "UTF16LE" === t && (a = (i = 255 & a) << 8 | a >>> 8),
                                s = (c = d + o) >>> 2; l.length <= s; )
                                    l.push(0);
                                l[s] |= a << 8 * (2 - c % 4),
                                d += 2
                            }
                        return {
                            value: l,
                            binLen: 8 * d + n
                        }
                    }
                    ;
                    break;
                case "B64":
                    n = l;
                    break;
                case "BYTES":
                    n = c;
                    break;
                case "ARRAYBUFFER":
                    try {
                        n = new ArrayBuffer(0)
                    } catch (e) {
                        throw Error("ARRAYBUFFER not supported by this environment")
                    }
                    n = u;
                    break;
                default:
                    throw Error("format must be HEX, TEXT, B64, BYTES, or ARRAYBUFFER")
                }
                return n
            }
            function b(e, t) {
                return e << t | e >>> 32 - t
            }
            function A(e, t) {
                return 32 < t ? (t -= 32,
                new o(e.b << t | e.a >>> 32 - t,e.a << t | e.b >>> 32 - t)) : 0 !== t ? new o(e.a << t | e.b >>> 32 - t,e.b << t | e.a >>> 32 - t) : e
            }
            function C(e, t) {
                return e >>> t | e << 32 - t
            }
            function v(e, t) {
                var n = null;
                n = new o(e.a,e.b);
                return 32 >= t ? new o(n.a >>> t | n.b << 32 - t & 4294967295,n.b >>> t | n.a << 32 - t & 4294967295) : new o(n.b >>> t - 32 | n.a << 64 - t & 4294967295,n.a >>> t - 32 | n.b << 64 - t & 4294967295)
            }
            function E(e, t) {
                return 32 >= t ? new o(e.a >>> t,e.b >>> t | e.a << 32 - t & 4294967295) : new o(0,e.a >>> t - 32)
            }
            function w(e, t, n) {
                return e & t ^ ~e & n
            }
            function S(e, t, n) {
                return new o(e.a & t.a ^ ~e.a & n.a,e.b & t.b ^ ~e.b & n.b)
            }
            function I(e, t, n) {
                return e & t ^ e & n ^ t & n
            }
            function O(e, t, n) {
                return new o(e.a & t.a ^ e.a & n.a ^ t.a & n.a,e.b & t.b ^ e.b & n.b ^ t.b & n.b)
            }
            function B(e) {
                return C(e, 2) ^ C(e, 13) ^ C(e, 22)
            }
            function j(e) {
                var t = v(e, 28)
                  , n = v(e, 34);
                return e = v(e, 39),
                new o(t.a ^ n.a ^ e.a,t.b ^ n.b ^ e.b)
            }
            function y(e) {
                return C(e, 6) ^ C(e, 11) ^ C(e, 25)
            }
            function k(e) {
                var t = v(e, 14)
                  , n = v(e, 18);
                return e = v(e, 41),
                new o(t.a ^ n.a ^ e.a,t.b ^ n.b ^ e.b)
            }
            function Q(e) {
                return C(e, 7) ^ C(e, 18) ^ e >>> 3
            }
            function T(e) {
                var t = v(e, 1)
                  , n = v(e, 8);
                return e = E(e, 7),
                new o(t.a ^ n.a ^ e.a,t.b ^ n.b ^ e.b)
            }
            function N(e) {
                return C(e, 17) ^ C(e, 19) ^ e >>> 10
            }
            function R(e) {
                var t = v(e, 19)
                  , n = v(e, 61);
                return e = E(e, 6),
                new o(t.a ^ n.a ^ e.a,t.b ^ n.b ^ e.b)
            }
            function M(e, t) {
                var n = (65535 & e) + (65535 & t);
                return ((e >>> 16) + (t >>> 16) + (n >>> 16) & 65535) << 16 | 65535 & n
            }
            function D(e, t, n, a) {
                var r = (65535 & e) + (65535 & t) + (65535 & n) + (65535 & a);
                return ((e >>> 16) + (t >>> 16) + (n >>> 16) + (a >>> 16) + (r >>> 16) & 65535) << 16 | 65535 & r
            }
            function V(e, t, n, a, r) {
                var i = (65535 & e) + (65535 & t) + (65535 & n) + (65535 & a) + (65535 & r);
                return ((e >>> 16) + (t >>> 16) + (n >>> 16) + (a >>> 16) + (r >>> 16) + (i >>> 16) & 65535) << 16 | 65535 & i
            }
            function F(e, t) {
                var n, a, r;
                return n = (65535 & e.b) + (65535 & t.b),
                r = (65535 & (a = (e.b >>> 16) + (t.b >>> 16) + (n >>> 16))) << 16 | 65535 & n,
                n = (65535 & e.a) + (65535 & t.a) + (a >>> 16),
                new o((65535 & (a = (e.a >>> 16) + (t.a >>> 16) + (n >>> 16))) << 16 | 65535 & n,r)
            }
            function U(e, t, n, a) {
                var r, i, s;
                return r = (65535 & e.b) + (65535 & t.b) + (65535 & n.b) + (65535 & a.b),
                s = (65535 & (i = (e.b >>> 16) + (t.b >>> 16) + (n.b >>> 16) + (a.b >>> 16) + (r >>> 16))) << 16 | 65535 & r,
                r = (65535 & e.a) + (65535 & t.a) + (65535 & n.a) + (65535 & a.a) + (i >>> 16),
                new o((65535 & (i = (e.a >>> 16) + (t.a >>> 16) + (n.a >>> 16) + (a.a >>> 16) + (r >>> 16))) << 16 | 65535 & r,s)
            }
            function P(e, t, n, a, r) {
                var i, s, c;
                return i = (65535 & e.b) + (65535 & t.b) + (65535 & n.b) + (65535 & a.b) + (65535 & r.b),
                c = (65535 & (s = (e.b >>> 16) + (t.b >>> 16) + (n.b >>> 16) + (a.b >>> 16) + (r.b >>> 16) + (i >>> 16))) << 16 | 65535 & i,
                i = (65535 & e.a) + (65535 & t.a) + (65535 & n.a) + (65535 & a.a) + (65535 & r.a) + (s >>> 16),
                new o((65535 & (s = (e.a >>> 16) + (t.a >>> 16) + (n.a >>> 16) + (a.a >>> 16) + (r.a >>> 16) + (i >>> 16))) << 16 | 65535 & i,c)
            }
            function L(e) {
                var t, n = 0, a = 0;
                for (t = 0; t < arguments.length; t += 1)
                    n ^= arguments[t].b,
                    a ^= arguments[t].a;
                return new o(a,n)
            }
            function z(e) {
                var t, n = [];
                if ("SHA-1" === e)
                    n = [1732584193, 4023233417, 2562383102, 271733878, 3285377520];
                else if (0 === e.lastIndexOf("SHA-", 0))
                    switch (n = [3238371032, 914150663, 812702999, 4144912697, 4290775857, 1750603025, 1694076839, 3204075428],
                    t = [1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225],
                    e) {
                    case "SHA-224":
                        break;
                    case "SHA-256":
                        n = t;
                        break;
                    case "SHA-384":
                        n = [new o(3418070365,n[0]), new o(1654270250,n[1]), new o(2438529370,n[2]), new o(355462360,n[3]), new o(1731405415,n[4]), new o(41048885895,n[5]), new o(3675008525,n[6]), new o(1203062813,n[7])];
                        break;
                    case "SHA-512":
                        n = [new o(t[0],4089235720), new o(t[1],2227873595), new o(t[2],4271175723), new o(t[3],1595750129), new o(t[4],2917565137), new o(t[5],725511199), new o(t[6],4215389547), new o(t[7],327033209)];
                        break;
                    default:
                        throw Error("Unknown SHA variant")
                    }
                else {
                    if (0 !== e.lastIndexOf("SHA3-", 0) && 0 !== e.lastIndexOf("SHAKE", 0))
                        throw Error("No SHA variants supported");
                    for (e = 0; 5 > e; e += 1)
                        n[e] = [new o(0,0), new o(0,0), new o(0,0), new o(0,0), new o(0,0)]
                }
                return n
            }
            function x(e, t) {
                var n, a, r, i, o, s, c, l = [];
                for (n = t[0],
                a = t[1],
                r = t[2],
                i = t[3],
                o = t[4],
                c = 0; 80 > c; c += 1)
                    l[c] = 16 > c ? e[c] : b(l[c - 3] ^ l[c - 8] ^ l[c - 14] ^ l[c - 16], 1),
                    s = 20 > c ? V(b(n, 5), a & r ^ ~a & i, o, 1518500249, l[c]) : 40 > c ? V(b(n, 5), a ^ r ^ i, o, 1859775393, l[c]) : 60 > c ? V(b(n, 5), I(a, r, i), o, 2400959708, l[c]) : V(b(n, 5), a ^ r ^ i, o, 3395469782, l[c]),
                    o = i,
                    i = r,
                    r = b(a, 30),
                    a = n,
                    n = s;
                return t[0] = M(n, t[0]),
                t[1] = M(a, t[1]),
                t[2] = M(r, t[2]),
                t[3] = M(i, t[3]),
                t[4] = M(o, t[4]),
                t
            }
            function H(e, t, n, a) {
                var r;
                for (r = 15 + (t + 65 >>> 9 << 4); e.length <= r; )
                    e.push(0);
                for (e[t >>> 5] |= 128 << 24 - t % 32,
                t += n,
                e[r] = 4294967295 & t,
                e[r - 1] = t / 4294967296 | 0,
                t = e.length,
                r = 0; r < t; r += 16)
                    a = x(e.slice(r, r + 16), a);
                return a
            }
            function q(e, t, n) {
                var a, r, i, s, c, l, u, d, h, p, g, f, m, b, A, C, v, E, L, z, x, H, q, J = [];
                if ("SHA-224" === n || "SHA-256" === n)
                    p = 64,
                    f = 1,
                    H = Number,
                    m = M,
                    b = D,
                    A = V,
                    C = Q,
                    v = N,
                    E = B,
                    L = y,
                    x = I,
                    z = w,
                    q = Z;
                else {
                    if ("SHA-384" !== n && "SHA-512" !== n)
                        throw Error("Unexpected error in SHA-2 implementation");
                    p = 80,
                    f = 2,
                    H = o,
                    m = F,
                    b = U,
                    A = P,
                    C = T,
                    v = R,
                    E = j,
                    L = k,
                    x = O,
                    z = S,
                    q = K
                }
                for (n = t[0],
                a = t[1],
                r = t[2],
                i = t[3],
                s = t[4],
                c = t[5],
                l = t[6],
                u = t[7],
                g = 0; g < p; g += 1)
                    16 > g ? (h = g * f,
                    d = e.length <= h ? 0 : e[h],
                    h = e.length <= h + 1 ? 0 : e[h + 1],
                    J[g] = new H(d,h)) : J[g] = b(v(J[g - 2]), J[g - 7], C(J[g - 15]), J[g - 16]),
                    d = A(u, L(s), z(s, c, l), q[g], J[g]),
                    h = m(E(n), x(n, a, r)),
                    u = l,
                    l = c,
                    c = s,
                    s = m(i, d),
                    i = r,
                    r = a,
                    a = n,
                    n = m(d, h);
                return t[0] = m(n, t[0]),
                t[1] = m(a, t[1]),
                t[2] = m(r, t[2]),
                t[3] = m(i, t[3]),
                t[4] = m(s, t[4]),
                t[5] = m(c, t[5]),
                t[6] = m(l, t[6]),
                t[7] = m(u, t[7]),
                t
            }
            function J(e, t) {
                var n, a, r, i, s = [], c = [];
                if (null !== e)
                    for (a = 0; a < e.length; a += 2)
                        t[(a >>> 1) % 5][(a >>> 1) / 5 | 0] = L(t[(a >>> 1) % 5][(a >>> 1) / 5 | 0], new o((255 & e[a + 1]) << 24 | (65280 & e[a + 1]) << 8 | (16711680 & e[a + 1]) >>> 8 | e[a + 1] >>> 24,(255 & e[a]) << 24 | (65280 & e[a]) << 8 | (16711680 & e[a]) >>> 8 | e[a] >>> 24));
                for (n = 0; 24 > n; n += 1) {
                    for (i = z("SHA3-"),
                    a = 0; 5 > a; a += 1)
                        s[a] = L(t[a][0], t[a][1], t[a][2], t[a][3], t[a][4]);
                    for (a = 0; 5 > a; a += 1)
                        c[a] = L(s[(a + 4) % 5], A(s[(a + 1) % 5], 1));
                    for (a = 0; 5 > a; a += 1)
                        for (r = 0; 5 > r; r += 1)
                            t[a][r] = L(t[a][r], c[a]);
                    for (a = 0; 5 > a; a += 1)
                        for (r = 0; 5 > r; r += 1)
                            i[r][(2 * a + 3 * r) % 5] = A(t[a][r], W[a][r]);
                    for (a = 0; 5 > a; a += 1)
                        for (r = 0; 5 > r; r += 1)
                            t[a][r] = L(i[a][r], new o(~i[(a + 1) % 5][r].a & i[(a + 2) % 5][r].a,~i[(a + 1) % 5][r].b & i[(a + 2) % 5][r].b));
                    t[0][0] = L(t[0][0], Y[n])
                }
                return t
            }
            var Z, K, W, Y;
            K = [new o((Z = [1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298])[0],3609767458), new o(Z[1],602891725), new o(Z[2],3964484399), new o(Z[3],2173295548), new o(Z[4],4081628472), new o(Z[5],3053834265), new o(Z[6],2937671579), new o(Z[7],3664609560), new o(Z[8],2734883394), new o(Z[9],1164996542), new o(Z[10],1323610764), new o(Z[11],3590304994), new o(Z[12],4068182383), new o(Z[13],991336113), new o(Z[14],633803317), new o(Z[15],3479774868), new o(Z[16],2666613458), new o(Z[17],944711139), new o(Z[18],2341262773), new o(Z[19],2007800933), new o(Z[20],1495990901), new o(Z[21],1856431235), new o(Z[22],3175218132), new o(Z[23],2198950837), new o(Z[24],3999719339), new o(Z[25],766784016), new o(Z[26],2566594879), new o(Z[27],3203337956), new o(Z[28],1034457026), new o(Z[29],2466948901), new o(Z[30],3758326383), new o(Z[31],168717936), new o(Z[32],1188179964), new o(Z[33],1546045734), new o(Z[34],1522805485), new o(Z[35],2643833823), new o(Z[36],2343527390), new o(Z[37],1014477480), new o(Z[38],1206759142), new o(Z[39],344077627), new o(Z[40],1290863460), new o(Z[41],3158454273), new o(Z[42],3505952657), new o(Z[43],106217008), new o(Z[44],3606008344), new o(Z[45],1432725776), new o(Z[46],1467031594), new o(Z[47],851169720), new o(Z[48],3100823752), new o(Z[49],1363258195), new o(Z[50],3750685593), new o(Z[51],3785050280), new o(Z[52],3318307427), new o(Z[53],3812723403), new o(Z[54],2003034995), new o(Z[55],3602036899), new o(Z[56],1575990012), new o(Z[57],1125592928), new o(Z[58],2716904306), new o(Z[59],442776044), new o(Z[60],593698344), new o(Z[61],3733110249), new o(Z[62],2999351573), new o(Z[63],3815920427), new o(3391569614,3928383900), new o(3515267271,566280711), new o(3940187606,3454069534), new o(4118630271,4000239992), new o(116418474,1914138554), new o(174292421,2731055270), new o(289380356,3203993006), new o(460393269,320620315), new o(685471733,587496836), new o(852142971,1086792851), new o(1017036298,365543100), new o(1126000580,2618297676), new o(1288033470,3409855158), new o(1501505948,4234509866), new o(1607167915,987167468), new o(1816402316,1246189591)],
            Y = [new o(0,1), new o(0,32898), new o(2147483648,32906), new o(2147483648,2147516416), new o(0,32907), new o(0,2147483649), new o(2147483648,2147516545), new o(2147483648,32777), new o(0,138), new o(0,136), new o(0,2147516425), new o(0,2147483658), new o(0,2147516555), new o(2147483648,139), new o(2147483648,32905), new o(2147483648,32771), new o(2147483648,32770), new o(2147483648,128), new o(0,32778), new o(2147483648,2147483658), new o(2147483648,2147516545), new o(2147483648,32896), new o(0,2147483649), new o(2147483648,2147516424)],
            W = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]],
            void 0 === (a = function() {
                return i
            });


	var get_signature = function() {
            var n = Date.now(),e = 'password',x = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
              , a = new i("SHA-1","TEXT");
            return a.setHMACKey("d1b964811afb40118a12068ff74a12f4", "TEXT"),
            a.update(e),
            a.update(x),
            a.update("com.zhihu.web"),
            a.update(String(n)),
            a.getHMAC("HEX")

        }