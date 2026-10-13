/* 1daily AG – Goldmarkt-Seite: Preisgrafik und Handelszeiten */
(function () {
  var EN = document.documentElement.lang === 'en';
  var sep = EN ? ',' : "'";
  var fmt = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, sep); };
  var NS = 'http://www.w3.org/2000/svg';

  /* 1) Goldpreis seit 2000 ----------------------------------------------- */
  var fig = document.querySelector('.gchart');
  if (fig) {
    var plot = fig.querySelector('.gc-plot');
    var tip = fig.querySelector('.gc-tip');
    var pts = JSON.parse(plot.getAttribute('data-pts'));
    var yMax = 5000, cur = -1, geo = null;

    var render = function () {
      var w = Math.max(280, plot.clientWidth), sm = w < 620;
      var h = sm ? 300 : 420;
      var m = { l: sm ? 44 : 62, r: sm ? 50 : 76, t: 30, b: 34 };
      var iw = w - m.l - m.r, ih = h - m.t - m.b;
      var x = function (i) { return m.l + iw * i / (pts.length - 1); };
      var y = function (v) { return m.t + ih * (1 - v / yMax); };
      var s = '<svg xmlns="' + NS + '" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" aria-hidden="true">';
      s += '<defs><linearGradient id="gcfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9B45E" stop-opacity=".42"/><stop offset="1" stop-color="#D9B45E" stop-opacity="0"/></linearGradient></defs>';
      s += '<g class="gc-grid gc-axis">';
      for (var v = 0; v <= yMax; v += 1000) {
        s += '<line x1="' + m.l + '" x2="' + (w - m.r) + '" y1="' + y(v) + '" y2="' + y(v) + '"/>';
        s += '<text x="' + (m.l - 10) + '" y="' + (y(v) + 4.5) + '" text-anchor="end">' + fmt(v) + '</text>';
      }
      pts.forEach(function (p, i) {
        if ((p[0] % 5) === 0) s += '<text x="' + x(i) + '" y="' + (h - 8) + '" text-anchor="middle">' + p[0] + '</text>';
      });
      s += '</g>';
      var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(p[1]).toFixed(1); }).join('');
      s += '<path class="gc-area" d="' + d + 'L' + x(pts.length - 1).toFixed(1) + ' ' + y(0) + 'L' + x(0) + ' ' + y(0) + 'Z"/>';
      s += '<path class="gc-line" pathLength="1000" d="' + d + '"/>';
      var f = pts[0], l = pts[pts.length - 1];
      s += '<circle class="gc-pt" cx="' + x(0) + '" cy="' + y(f[1]) + '" r="5"/>';
      s += '<circle class="gc-pt" cx="' + x(pts.length - 1) + '" cy="' + y(l[1]) + '" r="5"/>';
      s += '<text class="gc-lbl" x="' + (x(0) + 2) + '" y="' + (y(f[1]) - 14) + '">' + fmt(f[1]) + '</text>';
      s += '<text class="gc-lbl" x="' + (x(pts.length - 1) + 10) + '" y="' + (y(l[1]) + 5) + '">' + fmt(l[1]) + '</text>';
      s += '<text class="gc-lbl-s" x="' + (m.l) + '" y="14">' + (EN ? 'USD per troy ounce' : 'USD pro Feinunze') + '</text>';
      s += '<line class="gc-x" x1="0" x2="0" y1="' + m.t + '" y2="' + (h - m.b) + '" style="display:none"/>';
      s += '<circle class="gc-pt gc-hov" r="6" style="display:none"/>';
      s += '<rect class="gc-hit" x="' + m.l + '" y="0" width="' + iw + '" height="' + h + '"/>';
      s += '</svg>';
      plot.innerHTML = s;
      geo = { x: x, y: y, m: m, iw: iw, h: h };
      if (cur >= 0) show(cur);
    };

    var show = function (i) {
      cur = i;
      var svg = plot.querySelector('svg'), p = pts[i];
      var cx = geo.x(i), cy = geo.y(p[1]);
      var ln = svg.querySelector('.gc-x'), dot = svg.querySelector('.gc-hov');
      ln.setAttribute('x1', cx); ln.setAttribute('x2', cx); ln.style.display = '';
      dot.setAttribute('cx', cx); dot.setAttribute('cy', cy); dot.style.display = '';
      tip.innerHTML = '<b>' + fmt(p[1]) + ' USD</b>' + (EN ? 'Year-end ' : 'Jahresende ') + p[0];
      var left = Math.min(Math.max(cx, 70), plot.clientWidth - 70);
      tip.style.left = left + 'px'; tip.style.top = (cy - 10) + 'px';
      fig.classList.add('hovering');
    };
    var hide = function () {
      cur = -1; fig.classList.remove('hovering');
      var svg = plot.querySelector('svg');
      if (svg) { svg.querySelector('.gc-x').style.display = 'none'; svg.querySelector('.gc-hov').style.display = 'none'; }
    };
    plot.addEventListener('pointermove', function (e) {
      var r = plot.getBoundingClientRect(), px = e.clientX - r.left;
      var i = Math.round((px - geo.m.l) / geo.iw * (pts.length - 1));
      show(Math.max(0, Math.min(pts.length - 1, i)));
    });
    plot.addEventListener('pointerleave', hide);
    fig.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        var i = cur < 0 ? pts.length - 1 : cur + (e.key === 'ArrowRight' ? 1 : -1);
        show(Math.max(0, Math.min(pts.length - 1, i)));
      } else if (e.key === 'Escape') hide();
    });
    fig.addEventListener('blur', hide);
    render();
    var rt = null;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(render, 120); });
  }

  /* 2) Handelszeiten in Schweizer Zeit ----------------------------------- */
  var box = document.querySelector('.sess');
  if (!box || !window.Intl) return;
  var ZH = 'Europe/Zurich';
  var partsCache = {};
  var parts = function (tz, date) {
    var f = partsCache[tz] || (partsCache[tz] = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', weekday: 'short', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    var o = {};
    f.formatToParts(date).forEach(function (p) { o[p.type] = p.value; });
    o.h = (+o.hour) % 24; o.min = +o.minute;
    return o;
  };
  var offset = function (tz, date) {
    var p = parts(tz, date);
    return Math.round((Date.UTC(+p.year, +p.month - 1, +p.day, p.h, p.min, +p.second) - date.getTime()) / 60000);
  };
  var hm = function (s) { var a = s.split(':'); return (+a[0]) * 60 + (+a[1]); };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var clock = function (mins) { mins = ((mins % 1440) + 1440) % 1440; return pad(Math.floor(mins / 60)) + ':' + pad(mins % 60); };
  /* lokale Börsenzeit (heute in tz) → Minuten in Schweizer Zeit */
  var toZurich = function (tz, local, now) {
    var p = parts(tz, now);
    var guess = Date.UTC(+p.year, +p.month - 1, +p.day, 0, 0) + local * 60000;
    var inst = new Date(guess - offset(tz, new Date(guess)) * 60000);
    var z = parts(ZH, inst);
    return z.h * 60 + z.min;
  };
  var WD = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 0 };
  var rows = Array.prototype.slice.call(box.querySelectorAll('.sess-row'));
  var layer = box.querySelector('.sess-layer');
  var ov = layer.querySelector('.sess-ov'), nowEl = layer.querySelector('.sess-now');
  var status = document.querySelector('.sess-status');
  var pct = function (m) { return (m / 1440 * 100).toFixed(3) + '%'; };

  var cfdOpen = function (d) {
    var p = parts('America/New_York', d), t = p.h * 60 + p.min, wd = WD[p.weekday];
    if (wd === 6) return false;
    if (wd === 5 && t >= 17 * 60) return false;
    if (wd === 0 && t < 18 * 60) return false;
    return !(t >= 17 * 60 && t < 18 * 60);
  };
  var sessOpen = function (r, d) {
    var p = parts(r.tz, d), t = p.h * 60 + p.min, wd = WD[p.weekday];
    return wd >= 1 && wd <= 5 && t >= r.from && t < r.to;
  };

  var model = rows.map(function (el) {
    return { el: el, tz: el.getAttribute('data-tz'), from: hm(el.getAttribute('data-from')), to: hm(el.getAttribute('data-to')), name: el.getAttribute('data-name'), cfd: el.classList.contains('sess-cfd'), ov: el.hasAttribute('data-ov') };
  });

  var layout = function () {
    var now = new Date(), spans = {};
    model.forEach(function (r) {
      var a = toZurich(r.tz, r.from, now), b = toZurich(r.tz, r.to, now);
      var segs = b > a ? [[a, b]] : [[a, 1440], [0, b]];
      var t = r.el.querySelector('.sess-t');
      t.innerHTML = segs.filter(function (s) { return s[1] - s[0] > 0; }).map(function (s, k) {
        var lbl = k === 0 ? clock(a) + '–' + clock(b) : '';
        return '<div class="sess-b" style="left:' + pct(s[0]) + ';width:' + pct(s[1] - s[0]) + '"><span>' + lbl + '</span></div>';
      }).join('');
      if (r.cfd) {
        var label = segs.length > 1 ? (EN ? 'Daily break ' : 'Pause ') + clock(b) + '–' + clock(a) : '';
        t.setAttribute('title', label);
        var first = t.querySelector('.sess-b span');
        if (first) first.textContent = (EN ? 'Open ' : 'Offen ') + clock(a) + '–' + clock(b);
      }
      spans[r.name] = [a, b];
      r.za = a; r.zb = b;
    });
    var ovRows = model.filter(function (r) { return r.ov; });
    if (ovRows.length === 2) {
      var s = Math.max(ovRows[0].za, ovRows[1].za), e = Math.min(ovRows[0].zb, ovRows[1].zb);
      if (e > s) { ov.style.left = pct(s); ov.style.width = pct(e - s); ov.style.display = ''; ov.setAttribute('title', clock(s) + '–' + clock(e)); }
      else ov.style.display = 'none';
    }
    tick();
  };

  var nextOpen = function (now) {
    var d = new Date(Math.ceil(now.getTime() / 1800000) * 1800000);
    for (var i = 0; i < 400; i++) { if (cfdOpen(d)) return d; d = new Date(d.getTime() + 1800000); }
    return null;
  };
  var dayName = function (d) {
    try { return new Intl.DateTimeFormat(EN ? 'en-GB' : 'de-CH', { timeZone: ZH, weekday: 'long' }).format(d); } catch (e) { return ''; }
  };

  var tick = function () {
    var now = new Date(), z = parts(ZH, now), zm = z.h * 60 + z.min;
    nowEl.style.left = pct(zm); nowEl.style.display = 'block';
    nowEl.querySelector('b').textContent = (EN ? 'Now ' : 'Jetzt ') + clock(zm);
    var fr = zm / 1440, nb = nowEl.querySelector('b');
    nb.style.left = fr > 0.88 ? 'auto' : (fr < 0.12 ? '0' : '50%');
    nb.style.right = fr > 0.88 ? '0' : 'auto';
    nb.style.transform = (fr > 0.88 || fr < 0.12) ? 'none' : 'translateX(-50%)';
    if (!status) return;
    var txt, closed = false;
    if (cfdOpen(now)) {
      var open = model.filter(function (r) { return !r.cfd && sessOpen(r, now); }).map(function (r) { return r.name; });
      txt = EN ? 'XAUUSD is trading now. ' + (open.length ? 'Core hours: ' + open.join(', ') + '.' : 'The main exchanges are outside their core hours.')
               : 'XAUUSD ist jetzt handelbar. ' + (open.length ? 'In der Kernzeit: ' + open.join(', ') + '.' : 'Die Hauptbörsen sind ausserhalb ihrer Kernzeit.');
    } else {
      closed = true;
      var n = nextOpen(now), nz = n ? parts(ZH, n) : null, t = nz ? clock(nz.h * 60 + nz.min) : '';
      var sameDay = n && (n.getTime() - now.getTime()) < 6 * 3600000;
      if (sameDay) txt = EN ? 'Daily trading break. XAUUSD reopens at ' + t + ' Swiss time.' : 'Tägliche Handelspause. XAUUSD öffnet wieder um ' + t + ' Uhr Schweizer Zeit.';
      else txt = EN ? 'Weekend. XAUUSD reopens on ' + dayName(n) + ' at ' + t + ' Swiss time.' : 'Wochenende. XAUUSD öffnet wieder am ' + dayName(n) + ' um ' + t + ' Uhr Schweizer Zeit.';
    }
    status.classList.toggle('closed', closed);
    status.querySelector('span').textContent = txt;
  };

  layout();
  setInterval(tick, 30000);
  var lt = null;
  window.addEventListener('resize', function () { clearTimeout(lt); lt = setTimeout(layout, 150); });
})();
