import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool

PRESETS = [('Kawa na mieście', 15), ('Pizza na wynos', 45), ('Bilet do kina', 35), ('Subskrypcja streamingu', 50),
           ('Pełny bak paliwa', 300), ('Nowy smartfon', 4000), ('Flagowy smartfon', 6500), ('Czynsz za mieszkanie', 2500),
           ('Tydzień wakacji', 4000), ('Używany samochód', 40000)]
chips = ''.join(f'<button type="button" class="preset-btn" data-name="{html.escape(n)}" data-price="{p}">{html.escape(n)}</button>' for n, p in PRESETS)

main_inner = f'''    <p class="field-title" id="kindLabel">Twoja pensja</p>
    <div class="type-toggle" role="radiogroup" aria-labelledby="kindLabel">
      <label><input type="radio" name="kind" id="kGross" value="gross" checked><span>Brutto (umowa o pracę)</span></label>
      <label><input type="radio" name="kind" id="kNet" value="net"><span>Na rękę</span></label>
    </div>
    <div class="split-controls two">
      <div class="field"><label for="pay" id="payLbl">Pensja brutto miesięcznie (zł)</label><input type="number" id="pay" inputmode="decimal" value="7000" min="0" step="100"></div>
      <div class="field"><label for="hw">Godziny pracy w tygodniu</label><input type="number" id="hw" inputmode="decimal" value="40" min="1" max="80" step="1"><span class="hint">Pełny etat to 40 godzin.</span></div>
    </div>
    <div class="field"><label for="cm">Dojazd do pracy w obie strony dziennie (minuty)</label><input type="number" id="cm" inputmode="numeric" value="0" min="0" max="300" step="5"><span class="hint">Opcjonalnie — wtedy policzymy też Twoją realną stawkę, z czasem dojazdów.</span></div>

    <div class="net-box">
      <span class="label">Zarabiasz na rękę</span>
      <span class="net-amount" id="ph">0 zł/godz.</span>
      <span class="pct" id="phNote"></span>
    </div>

    <p class="field-title">Ile godzin pracy to kosztuje?</p>
    <div class="presets">{chips}</div>
    <div class="split-controls two">
      <div class="field"><label for="iname">Co chcesz kupić</label><input type="text" id="iname" value="Flagowy smartfon" maxlength="40" autocomplete="off"></div>
      <div class="field"><label for="iprice">Cena (zł)</label><input type="number" id="iprice" inputmode="decimal" value="6500" min="0" step="10"></div>
    </div>
    <div class="cost-box" aria-live="polite">
      <span class="cost-big" id="cost">0 godz.</span>
      <span class="cost-note" id="costNote"></span>
    </div>

    <div class="share-row">
      <button type="button" class="download-btn" id="storyBtn">Grafika do relacji (Instagram)</button>
      <button type="button" class="download-btn story-btn" id="shareBtn">Udostępnij link</button>
      <span class="hint" id="shareStatus" aria-live="polite"></span>
    </div>

    <div class="tbl-wrap">
    <table class="data-table hours">
      <caption>Ile pracy kosztują codzienne wydatki — przy Twojej stawce</caption>
      <thead><tr><th scope="col">Wydatek</th><th scope="col">Cena</th><th scope="col">Czas pracy</th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
    </div>
    <div class="verdict" id="verdict"></div>'''

trust = ('<strong>Stawka na rękę</strong> to pensja netto podzielona przez godziny pracy w miesiącu: przy 40 godzinach tygodniowo średnio 167,3 godziny (2008 godzin w 2026 i 2027 r. ÷ 12). '
         'Netto z kwoty brutto liczymy jak na umowie o pracę (składki 13,71%, zdrowotna 9%, podatek 12% z PIT-2, bez PPK). '
         '<strong>Realna stawka</strong> uwzględnia też czas dojazdów w dniach roboczych — to pomysł znany z klasycznej książki „Your Money or Your Life” Vicki Robin i Joe Domingueza: każda rzecz kosztuje nie tylko złotówki, ale też godziny Twojego życia. '
         'Ceny w przykładach są orientacyjne — wpisz własne.')

more = ('<a href="kalkulator-budzetu.html">Budżet 50/30/20 — podział wypłaty →</a><br>'
        '<a href="../artykuly/psychologia-wydawania-pieniedzy.html">Jak przestać wydawać pieniądze — psychologia wydawania →</a><br>'
        '<a href="czy-dobrze-zarabiam.html">Czy dobrze zarabiam? →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function fmt2(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(r2(n)) + ' zł'; }
  function num(id, max){ var v = parseFloat($(id).value); if (!isFinite(v) || v < 0) v = 0; return max != null ? Math.min(v, max) : v; }
  function netEtat(g){
    var zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245)), h = r2((g - zus) * 0.09);
    var tax = Math.max(0, Math.round(Math.max(0, Math.round(g - zus - 250)) * 0.12 - 300));
    return g - zus - h - tax;
  }
  function plural(n, one, few, many){ var a = Math.abs(n) % 100, b = a % 10; if (n === 1) return one; if (b >= 2 && b <= 4 && (a < 12 || a > 14)) return few; return many; }
  /* czas pracy po polsku: „45 min”, „3 godz. 20 min”, „61 godz. (ok. 8 dni pracy)” */
  function dur(h, hpd){
    var m = Math.round(h * 60);
    if (m < 60) return m + ' min';
    var H = Math.floor(m / 60), M = m % 60;
    var s = H < 10 ? H + ' godz.' + (M ? ' ' + M + ' min' : '') : Math.round(h) + ' godz.';
    if (h >= hpd * 2) s += ' (ok. ' + Math.round(h / hpd) + ' ' + plural(Math.round(h / hpd), 'dzień', 'dni', 'dni') + ' pracy)';
    return s;
  }
  function durShort(h){ var m = Math.round(h * 60); if (m < 60) return m + ' minut'; var H = Math.round(h); return H + ' ' + plural(H, 'godzinę', 'godziny', 'godzin'); }
  var PRE = ''' + str([[n, p] for n, p in PRESETS]).replace("'", '"') + r''';
  var last = null;
  function recalc(){
    var isNet = $('kNet').checked, pay = num('pay'), hw = Math.max(1, num('hw', 80)), cm = num('cm', 300);
    $('payLbl').textContent = isNet ? 'Pensja na rękę miesięcznie (zł)' : 'Pensja brutto miesięcznie (zł)';
    var net = isNet ? pay : Math.max(0, netEtat(pay));
    var hm = 2008 / 12 * hw / 40, hpd = hw / 5;
    var rate = hm ? net / hm : 0;
    var real = hm ? net / (hm + cm / 60 * 251 / 12) : 0;
    $('ph').textContent = fmt2(rate) + '/godz.';
    var note = 'czyli ' + fmt2(rate / 60) + ' na minutę · ' + fmt(net) + ' na rękę ÷ ' + Math.round(hm) + ' godz. w miesiącu';
    if (cm > 0) note += ' · realnie, z dojazdami: ' + fmt2(real) + ' / godz.';
    $('phNote').textContent = note;
    var name = $('iname').value.trim() || 'To', price = num('iprice');
    var h = rate ? price / rate : 0;
    $('cost').textContent = rate ? dur(h, hpd) : '—';
    $('costNote').textContent = rate ? name + ' za ' + fmt(price) + ' to tyle Twojej pracy' + (cm > 0 ? ' — a z dojazdami ' + dur(price / real, hpd) : '') + '.' : 'Wpisz pensję.';
    $('rows').innerHTML = PRE.map(function(p){ return '<tr><td>' + p[0] + '</td><td>' + fmt(p[1]) + '</td><td>' + (rate ? dur(p[1] / rate, hpd) : '—') + '</td></tr>'; }).join('') +
      '<tr class="em"><td>Codzienna kawa przez rok (250 dni)</td><td>' + fmt(15 * 250) + '</td><td>' + (rate ? dur(3750 / rate, hpd) : '—') + '</td></tr>';
    $('verdict').textContent = rate ? 'Kawa za 15 zł w każdy dzień roboczy to ' + fmt(3750) + ' rocznie — ' + durShort(3750 / rate) + ' Twojej pracy. Nie chodzi o to, żeby z niej rezygnować, tylko żeby wydawać świadomie: czy ta rzecz jest warta tylu godzin?' : '';
    last = {name: name, price: price, h: h, rate: rate};
    queueStory();
  }

  /* grafika 1080×1920 do relacji */
  var storyBlob = null, storyKey = '', storyTimer = null, fontsReady = null;
  function curKey(){ return last ? last.name + '|' + Math.round(last.price) + '|' + Math.round(last.h * 60) : ''; }
  function loadFonts(){
    if (fontsReady) return fontsReady;
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = '../assets/fonts/fonts.css'; document.head.appendChild(l);
    fontsReady = new Promise(function(res){ l.onload = res; l.onerror = res; }).then(function(){
      return Promise.all(['600 100px Fraunces', '500 60px Fraunces', '500 60px Inter', '600 60px Inter'].map(function(f){ return document.fonts.load(f, 'ąęłśćżźóń%0'); })).catch(function(){});
    });
    return fontsReady;
  }
  function rr(c, x, y, w, h, r){ c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function wrap(c, text, x, y, maxW, lh){
    var words = text.split(' '), line = '', lines = [];
    words.forEach(function(w){ var t = line ? line + ' ' + w : w; if (c.measureText(t).width > maxW && line){ lines.push(line); line = w; } else line = t; });
    if (line) lines.push(line);
    lines.forEach(function(l, i){ c.fillText(l, x, y + i * lh); });
    return y + (lines.length - 1) * lh;
  }
  function drawStory(){
    if (!last || !last.rate) return;
    var key = curKey();
    var cv = document.createElement('canvas'); cv.width = 1080; cv.height = 1920; var c = cv.getContext('2d');
    var g = c.createLinearGradient(0, 0, 1080, 1920); g.addColorStop(0, '#1b2a22'); g.addColorStop(1, '#0a100c'); c.fillStyle = g; c.fillRect(0, 0, 1080, 1920);
    var rg = c.createRadialGradient(880, 460, 0, 880, 460, 760); rg.addColorStop(0, 'rgba(224,166,63,0.22)'); rg.addColorStop(1, 'rgba(224,166,63,0)'); c.fillStyle = rg; c.fillRect(0, 0, 1080, 1920);
    var F = '"Fraunces", Georgia, serif', I = '"Inter", system-ui, sans-serif';
    c.textBaseline = 'alphabetic'; c.textAlign = 'left';
    c.fillStyle = '#e0a63f'; c.font = '600 40px ' + I; c.fillText('ILE GODZIN PRACY TO KOSZTUJE?', 90, 330);
    c.fillStyle = '#eef2ef'; c.font = '500 70px ' + F;
    var y = wrap(c, last.name + ' (' + fmt(last.price) + ')', 90, 520, 900, 84);
    c.font = '500 62px ' + I; c.fillText('kosztuje mnie', 90, y + 110);
    var m = Math.round(last.h * 60), big, unit;
    if (m < 60){ big = String(m); unit = plural(m, 'minutę pracy', 'minuty pracy', 'minut pracy'); }
    else { var H = Math.round(last.h); big = String(H); unit = plural(H, 'godzinę pracy', 'godziny pracy', 'godzin pracy'); }
    c.fillStyle = '#e0a63f'; c.font = '600 ' + (big.length > 3 ? 260 : 330) + 'px ' + F; c.fillText(big, 78, y + 440);
    c.fillStyle = '#eef2ef'; c.font = '500 66px ' + I; c.fillText(unit, 90, y + 550);
    c.fillStyle = '#3ad889'; rr(c, 90, 1390, 900, 150, 32); c.fill();
    c.fillStyle = '#08130d'; c.font = '600 52px ' + I; c.textAlign = 'center'; c.fillText('Policz swoje rzeczy →', 540, 1485); c.textAlign = 'left';
    c.strokeStyle = '#3ad889'; c.lineWidth = 6; c.beginPath(); c.arc(118, 1650, 28, 0, Math.PI * 2); c.stroke();
    c.beginPath(); c.moveTo(103, 1658); c.lineTo(115, 1646); c.lineTo(124, 1653); c.lineTo(136, 1640); c.stroke();
    c.fillStyle = '#ffffff'; c.font = '500 56px ' + F; c.fillText('Mądry Portfel', 166, 1670);
    c.fillStyle = '#a8b6ae'; c.font = '500 36px ' + I; c.fillText('bartuniadev.github.io/madry-portfel', 90, 1745);
    cv.toBlob(function(b){ storyBlob = b; storyKey = key; }, 'image/jpeg', 0.92);
  }
  var storyIdle = false;
  function queueStory(){ if (!storyIdle) return; if (storyBlob && storyKey === curKey()) return; clearTimeout(storyTimer); storyTimer = setTimeout(function(){ loadFonts().then(drawStory); }, 300); }
  $('storyBtn').addEventListener('click', function(){
    var st = $('shareStatus');
    if (!storyBlob || storyKey !== curKey()){ st.textContent = 'Przygotowuję grafikę — kliknij jeszcze raz za chwilę.'; storyIdle = true; queueStory(); return; }
    var file = new File([storyBlob], 'ile-godzin-pracy.jpg', {type: 'image/jpeg'});
    if (navigator.canShare && navigator.canShare({files: [file]})){ navigator.share({files: [file], title: 'Ile godzin pracy to kosztuje?'}).catch(function(){}); return; }
    var a = document.createElement('a'); a.href = URL.createObjectURL(storyBlob); a.download = 'ile-godzin-pracy.jpg';
    document.body.appendChild(a); a.click(); a.remove();
    st.textContent = 'Zapisano grafikę — wrzuć ją do relacji i dodaj naklejkę z linkiem do strony.';
  });
  $('shareBtn').addEventListener('click', function(){
    var url = 'https://bartuniadev.github.io/madry-portfel/narzedzia/ile-zarabiam-na-godzine.html';
    var text = last && last.rate ? last.name + ' kosztuje mnie ' + durShort(last.h) + ' pracy. Sprawdź, ile kosztuje Ciebie:' : 'Ile godzin pracy kosztują Twoje wydatki?';
    var st = $('shareStatus');
    if (navigator.share){ navigator.share({title: 'Ile godzin pracy to kosztuje?', text: text, url: url}).catch(function(){}); return; }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text + ' ' + url).then(function(){ st.textContent = 'Skopiowano — wklej znajomym.'; }, function(){ st.textContent = url; });
    else st.textContent = url;
  });
  document.querySelectorAll('.preset-btn').forEach(function(b){ b.addEventListener('click', function(){ $('iname').value = b.getAttribute('data-name'); $('iprice').value = b.getAttribute('data-price'); recalc(); }); });
  ['pay','hw','cm','iname','iprice','kGross','kNet'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  recalc();
  (window.requestIdleCallback || function(cb){ setTimeout(cb, 2500); })(function(){ storyIdle = true; queueStory(); }, {timeout: 4000});'''

css = '''  .presets{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 12px;}
  .preset-btn{font:inherit;font-size:0.85rem;cursor:pointer;color:var(--text);background:var(--surface-2);border:1px solid var(--border);border-radius:999px;padding:7px 12px;}
  .preset-btn:hover{border-color:var(--green);}
  .preset-btn:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  #iname{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 10px;font-size:1rem;font-family:inherit;min-height:44px;}
  .cost-box{display:grid;gap:4px;margin:6px 0 4px;padding:16px 18px;border-radius:12px;background:var(--surface-2);border:1px solid var(--border);}
  .cost-big{font-size:2rem;font-weight:700;color:#e0a63f;font-variant-numeric:tabular-nums;line-height:1.15;}
  .cost-note{font-size:0.9rem;color:var(--text-2);}
  .share-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:16px;}
  .share-row .download-btn{border:0;cursor:pointer;font-family:inherit;}
  .share-row .story-btn{background:var(--surface-2);color:var(--text);border:1px solid var(--border);}
  .share-row .hint{font-size:0.82rem;color:var(--text-2);overflow-wrap:anywhere;}
  .hours tr.em td{font-weight:700;color:#e0a63f;}
'''
print('godzina', make_tool.build('ile-zarabiam-na-godzine',
    'Ile zarabiam na godzinę? Cena w godzinach pracy',
    'Przelicz pensję na stawkę za godzinę i minutę na rękę i sprawdź, ile godzin pracy kosztuje smartfon, czynsz czy codzienna kawa. Z grafiką do udostępnienia.',
    'Ile zarabiam na godzinę — kalkulator', 'ile zarabiam na godzinę, stawka godzinowa netto, ile godzin pracy kosztuje, kalkulator stawki godzinowej, ile zarabiam na minutę',
    'Ile zarabiam na godzinę', 'Ile zarabiam na godzinę — i ile godzin pracy kosztują Twoje wydatki',
    'Wpisz pensję, a policzę, ile zarabiasz na rękę za godzinę i za minutę — także realnie, z czasem dojazdów. Potem sprawdź, ile godzin pracy kosztuje rzecz, którą chcesz kupić. Wszystko liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, css))
