function RandomNum(min, max) {
    return Math.floor(Math.random() * (max - min)) + min + 1
}

function RandomChoice(arr) {
    return arr[Math.floor(Math.random() * arr.length)]
}

function generateTrace(distance) {
    distance = Math.floor(distance);
    var trace = [];
    var sy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0];
    var st = [15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17,
        18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 14, 16, 17, 18, 16, 17, 18, 19, 20, 17];

    if (distance < 95) {
        var sx = [1, 2, 1, 2, 1, 2, 1, 1, 2, 1];
    } else {
        var sx = [1, 2, 1, 2, 1, 2, 2, 2, 3, 4];
    }
    var zt = RandomNum(20, 100);
    var baseX = RandomNum(530, 570),
        baseY = RandomNum(400, 420),
        zx = 0,
        zy = 0;
    var random_x = RandomNum(9, 14);
    trace.push([baseX, baseY, zt]);
    var n = 0, x = 0, y = 0, t = 0;
    while (true) {
        n += 1;
        if (n < 5) {
            x = 1;
        } else {
            x = RandomChoice(sx)
        }
        if (distance > 125 && random_x === n) {
            x = RandomNum(14, 18)
        }
        y = RandomChoice(sy);
        t = RandomChoice(st);
        zx += x;
        zy += y;
        trace.push([zx + baseX, zy + baseY, t]);
        if (distance - zx < 6) {
            break;
        }
    }
    var value = distance - zx;
    for (var i = 0; i < value; i++) {
        t = RandomChoice(st);

        if (value === i + 1) {
            t = RandomNum(42, 56)
        }
        if (value === i + 2) {
            t = RandomNum(32, 38)
        }
        if (value === i + 3) {
            t = RandomNum(30, 36)
        }
        x = 1;
        zx += x;
        trace.push([zx + baseX, zy + baseY, t]);
    }
    t = RandomNum(100, 200);
    trace.push([zx + baseX, zy + baseY, t]);
    return trace;
}

function generateTraceByPoints(points) {
    var move = [];
    (function () {
        function sp(p, p2, pp) {
            var sump = Math.abs(p - p2);
            var x3 = Math.floor(Math.abs((pp - p)) / sump * 100);
            if (sump > 200) {
                if (x3 < 5 || x3 > 95) return 1;
                if (x3 < 10 || x3 > 90) return 2;
                if (x3 < 50 || x3 > 50) return 4
            } else if (sump > 150) {
                if (x3 <= 10 || x3 >= 90) return 1;
                if (x3 <= 25 || x3 >= 75) return 2;
                if (x3 <= 40 || x3 >= 70) return 3;
                if (x3 <= 50 || x3 >= 50) return 4;
            } else if (sump > 100) {
                if (x3 <= 10 || x3 >= 90) return 1;
                if (x3 <= 15 || x3 >= 70) return 2;
                if (x3 <= 25 || x3 >= 60) return 3;
                if (x3 <= 50 || x3 >= 50) return 4;
            } else if (sump > 70) {
                if (x3 <= 15 || x3 >= 95) return 1;
                if (x3 <= 20 || x3 >= 80) return 2;
                if (x3 <= 25 || x3 >= 70) return 3;
                if (x3 <= 50 || x3 >= 50) return 4;
            } else {
                if (x3 <= 15 || x3 >= 80) return 0;
                if (x3 <= 25 || x3 >= 65) return 1;
                if (x3 <= 50 || x3 >= 50) return 2;
            }
        }

        function computeTime(distance) {
            var t;
            switch (distance) {
                case 0:
                    t = RandomNum(25, 69);
                    break;
                case 1:
                    t = RandomNum(13, 27);
                    break;
                case 2:
                    t = RandomNum(8, 15);
                    break;
                case 3:
                    t = RandomNum(7, 9);
                    break;
                case 4:
                    t = RandomNum(6, RandomNum(6, 9));
                    break;
            }
            return t;
        }

        var x = 0, y = 0;
        var distanceX = 3;
        var distanceY = 1;
        // 档速
        var s0 = [0, 1, 1, 1];
        var s1 = [1, 1, 2, 2];
        var s2 = [2, 2, 3, 3];
        var s3 = [2, 3, 4, 4];
        var s4 = [3, 4, 4, 4];
        var speed = [s0, s1, s2, s3, s4];
        var sditance;
        x = points[0].x;
        y = points[0].y;
        var time = 0;

        var c = points.length;
        move.push([x, y, RandomNum(100, 200)]);
        for (var i = 1; i < points.length; i++) {
            x2 = points[i].x;
            y2 = points[i].y;
            var o = Math.abs(points[i - 1].x - x2) / Math.abs(points[i - 1].y - y2);
            while (x - x2 !== 0 || y - y2 !== 0) {
                var xx = x - x2, yy = y - y2;
                var c = Math.abs(points[i - 1].x - x2) > Math.abs(points[i - 1].y - y2) ? 0 : 1;  //0=x 1=y谁是主线
                distanceX = sp(points[i - 1].x, x2, x);
                distancey = sp(points[i - 1].y, y2, y);
                if (!distanceX) {
                    distanceX = RandomNum(2, 4)
                }
                var addX = speed[distanceX][RandomNum(0, speed[distanceX].length - 1)];
                if (xx !== 0) {
                    // if (addX > xx)
                    // add=xx;
                    // x - x2 > 0 ? addX : - addX;
                    addX = xx > 0 ? -(addX > xx ? xx : addX) : (addX > Math.abs(xx) ? Math.abs(xx) : addX);
                    x += addX;
                }
                var ss = Math.round(Math.abs(points[i - 1].x - x) / o);
                ss = points[i - 1].y > y2 ? -ss : ss;
                y = ss + points[i - 1].y;
                move.push([x, y, computeTime(distanceX)])
            }
        }
        move.push([x, y, RandomNum(100, 200)]);
    })();
    return move
}

function encryptSlide(sid, distance, yy) {
    var encrypter = window._dx["UA"]["init"]({
        "token": sid
    });
    var trace = generateTrace(distance);
    encrypter["bindDomEvents"]();
    ms.mousedown({
        pageX: trace[0][0],
        pageY: trace[0][1],
        t: trace[0][2],
        button: 0
    });
    for (var i = 1; i < trace.length - 1; i++) {
        ms.mousemove({
            pageX: trace[i][0],
            pageY: trace[i][1],
            button: 0
        });
        sTimeout(trace[i][2]);
    }
    ms.mouseup({
        pageX: trace[trace.length - 1][0],
        pageY: trace[trace.length - 1][1],
        t: trace[trace.length - 1][2],
        button: 0
    });
    encrypter["sendSA"]();
    encrypter["sendTemp"]("x=" + distance + "&y=" + yy);
    return encrypter["getUA"]()
}

function encryptPosition(sid, position) {
    var encrypter = window._dx["UA"]["init"]({
        "token": sid
    });
    encrypter["bindDomEvents"]();
    var tracks;
    for (var i = 0; i < position.length; i++) {
        if (i === 0) {
            tracks = generateTraceByPoints([{
                'x': RandomNum(530, 570),
                'y': RandomNum(400, 420)
            }, {
                'x': position[0][0],
                'y': position[0][1]
            }]);
        } else {
            tracks = generateTraceByPoints([{
                'x': position[i - 1][0],
                'y': position[i - 1][0]
            }, {
                'x': position[i][0],
                'y': position[i][1]
            }]);
        }
        for (var j = 1; j < tracks.length - 1; j++) {
            ms.mousemove({
                pageX: tracks[j][0],
                pageY: tracks[j][1],
                button: 0
            });
            // sTimeout(tracks[i][2]);
        }
        ms.click({
            target: {
                className: "dx_captcha_clickword_hits"
            },
            offsetX: position[i][0],
            offsetY: position[i][1],
        });
    }
    encrypter["sendCA"]();
    return encrypter["getUA"]()
}

function encryptPosition2(sid, position) {
    var encrypter = window._dx["UA"]["init"]({
        "token": sid
    });
    encrypter["bindDomEvents"]();
    var trace = generateTraceByPoints([{
        'x': RandomNum(530, 570),
        'y': RandomNum(400, 420)
    }, {
        'x': position[0] + RandomNum(530, 570),
        'y': position[1] + RandomNum(250, 270)
    }]);
    for (var i = 1; i < trace.length - 1; i++) {
        ms.mousemove({
            pageX: trace[i][0],
            pageY: trace[i][1],
            button: 0
        });
        // sTimeout(trace[i][2]);
    }
    ms.mousedown({
        pageX: trace[trace.length - 1][0],
        pageY: trace[trace.length - 1][1],
        t: trace[trace.length - 1][2],
        button: 0
    });
    encrypter["sendSA"]();
    encrypter["sendTemp"]("x=" + position[0] + "&y=" + position[1]);
    return encrypter["getUA"]()
}
