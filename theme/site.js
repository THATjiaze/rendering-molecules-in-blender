/* Small conveniences. The pages read fine without any of this. */
(function () {
  'use strict';
  var root = document.documentElement;
  var all = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  var store = {
    get: function (key) { try { return localStorage.getItem(key); } catch (e) { return null; } },
    set: function (key, value) { try { localStorage.setItem(key, value); } catch (e) {} }
  };

  /* Theme: follows the system until the reader picks one. */
  var dark = window.matchMedia('(prefers-color-scheme: dark)');
  var isDark = function () { return root.dataset.theme ? root.dataset.theme === 'dark' : dark.matches; };
  var themeButtons = all('.theme-toggle');
  var labelTheme = function () { themeButtons.forEach(function (b) { b.textContent = isDark() ? 'Light theme' : 'Dark theme'; }); };
  themeButtons.forEach(function (b) {
    b.hidden = false;
    b.addEventListener('click', function () {
      root.dataset.theme = isDark() ? 'light' : 'dark';
      store.set('theme', root.dataset.theme);
      labelTheme();
    });
  });
  labelTheme();
  if (dark.addEventListener) dark.addEventListener('change', labelTheme);

  /* Contents drawer (narrow windows, and the front page). */
  var toggle = document.querySelector('.nav-toggle');
  var rail = document.getElementById('rail');
  var setNav = function (open) {
    root.classList.toggle('nav-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
  };
  if (toggle && rail) {
    toggle.addEventListener('click', function () {
      var open = !root.classList.contains('nav-open');
      setNav(open);
      if (open) { var first = rail.querySelector('a, input'); if (first) first.focus(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('nav-open')) { setNav(false); toggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!root.classList.contains('nav-open')) return;
      if (e.target.closest('.nav-toggle')) return;
      if (!e.target.closest('#rail') || e.target.closest('#rail a')) setNav(false);
    });
  }

  /* Mark the chapter being read in the contents list. */
  var chapterLinks = {};
  all('.chapters a').forEach(function (a) { chapterLinks[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window && Object.keys(chapterLinks).length) {
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var link = chapterLinks[entry.target.getAttribute('aria-labelledby')];
        if (!link || link === current) return;
        if (current) { current.classList.remove('is-active'); current.removeAttribute('aria-current'); }
        link.classList.add('is-active'); link.setAttribute('aria-current', 'location');
        current = link;
        if (window.matchMedia('(min-width: 62rem)').matches && link.scrollIntoView) link.scrollIntoView({ block: 'nearest' });
      });
    }, { rootMargin: '-15% 0px -75% 0px' });
    all('.chapter').forEach(function (c) { spy.observe(c); });
  }

  /* Exercises ticked as done, kept in this browser. */
  var done = {};
  try { done = JSON.parse(store.get('done') || '{}') || {}; } catch (e) { done = {}; }
  var boxes = all('.done input');
  var progress = document.querySelector('.progress');
  var showProgress = function () {
    if (!progress) return;
    var n = boxes.filter(function (b) { return b.checked; }).length;
    progress.hidden = n === 0;
    progress.querySelector('.progress-count').textContent = n;
  };
  boxes.forEach(function (box) {
    box.parentNode.hidden = false;
    box.checked = !!done[box.dataset.exercise];
    box.addEventListener('change', function () {
      if (box.checked) done[box.dataset.exercise] = 1; else delete done[box.dataset.exercise];
      store.set('done', JSON.stringify(done));
      showProgress();
    });
  });
  showProgress();

  /* "Show all answers" for a chapter's questions. */
  all('.check').forEach(function (block) {
    var button = block.querySelector('.reveal');
    var answers = all('details', block);
    if (!button || !answers.length) return;
    button.hidden = false;
    var label = function () { button.textContent = answers.every(function (d) { return d.open; }) ? 'Hide all answers' : 'Show all answers'; };
    button.addEventListener('click', function () {
      var open = !answers.every(function (d) { return d.open; });
      answers.forEach(function (d) { d.open = open; });
      label();
    });
    answers.forEach(function (d) { d.addEventListener('toggle', label); });
  });

  /* Search: the index is a script, loaded the first time the box is used, so it also works from a folder on disk. */
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var partsList = document.querySelector('.parts');
  var index = null, loading = false;
  var escapeHtml = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var load = function () {
    if (index || loading) return;
    loading = true;
    var s = document.createElement('script');
    s.src = 'assets/search-index.js';
    s.onload = function () {
      index = (window.SEARCH_INDEX || []).map(function (e) { return { e: e, title: e.t.toLowerCase(), text: e.x.toLowerCase() }; });
      run();
    };
    document.head.appendChild(s);
  };
  var run = function () {
    if (!input || !results) return;
    var words = input.value.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!words.length || !index) { results.hidden = true; results.innerHTML = ''; if (partsList) partsList.hidden = false; return; }
    var hits = [], phrase = words.join(' ');
    index.forEach(function (item) {
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        var inTitle = item.title.indexOf(words[i]) !== -1, at = item.text.indexOf(words[i]);
        if (!inTitle && at === -1) return;
        score += inTitle ? 12 : 1;
        if (at !== -1) score += Math.min(item.text.split(words[i]).length - 1, 5);
      }
      var whole = item.text.indexOf(phrase);
      if (words.length > 1) score += (item.title.indexOf(phrase) !== -1 ? 30 : 0) + (whole !== -1 ? 10 + Math.min(item.text.split(phrase).length - 1, 6) * 2 : 0);
      hits.push({ item: item, score: score, at: whole !== -1 ? whole : item.text.indexOf(words[0]) });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    var pattern = new RegExp('(' + words.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
    results.innerHTML = hits.slice(0, 24).map(function (h) {
      var e = h.item.e, at = Math.max(0, h.at - 50);
      var snippet = (at > 0 ? '…' : '') + e.x.slice(at, at + 150);
      return '<li><a href="' + e.u + '"><span class="hit-title">' + escapeHtml(e.t).replace(pattern, '<mark>$1</mark>') + '</span>' +
        '<span class="hit-where">' + escapeHtml(e.w) + '</span>' +
        '<span class="hit-text">' + escapeHtml(snippet).replace(pattern, '<mark>$1</mark>') + '</span></a></li>';
    }).join('') || '<li class="none">Nothing found for that.</li>';
    results.hidden = false;
    if (partsList) partsList.hidden = true;
  };
  if (input && results) {
    input.addEventListener('focus', load);
    input.addEventListener('input', function () { load(); run(); });
    input.addEventListener('keydown', function (e) { if (e.key === 'Escape' && input.value) { input.value = ''; run(); e.stopPropagation(); } });
  }
})();
