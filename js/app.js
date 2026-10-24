/* Sutadhana course app: group pages, lessons, reader, word review, grammar guide.
   All content lives in data/: groups/<id>.json (one per course group),
   library/<text>.json (shared texts, analysed word by word), grammar/index.json. */
(function () {
  "use strict";

  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const VERSION = "1";
  const PREVIEW = /[?&]preview\b/.test(location.search);
  const DAY = 86400000;
  const LEARNED_DAYS = 21;
  const NEW_PER_DAY = 20;

  /* ---------------- storage (per device; wrapped because it can be blocked) ---------------- */
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } },
  };

  /* ---------------- data loading ---------------- */
  const cache = {};
  async function load(path) {
    if (!cache[path]) {
      cache[path] = fetch(`data/${path}?v=${VERSION}-${state.dataVersion || ""}`, { cache: "no-cache" })
        .then((r) => { if (!r.ok) throw new Error(path); return r.json(); });
    }
    return cache[path];
  }
  const state = { dataVersion: "", group: null, gid: null, deck: null, lastReader: null, audio: null };
  const HP_ICON = `<svg class="hp" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1v-6h3zM3 19a2 2 0 0 0 2 2h1v-6H3z"/></svg>`;

  async function getGroup(gid) {
    if (state.group && state.gid === gid) return state.group;
    const g = await load(`groups/${gid}.json`);
    state.group = g; state.gid = gid; state.deck = null;
    return g;
  }
  const visibleLessons = (g) => g.lessons.filter((l) => l.published || PREVIEW).sort((a, b) => a.n - b.n);
  const publishedLessons = (g) => g.lessons.filter((l) => l.published).sort((a, b) => a.n - b.n);
  const lessonTexts = (l) => l.items.filter((i) => i.text).map((i) => i.text);

  /* ---------------- review deck ---------------- */
  // sc: undefined = the main review of all lessons; a lesson number = that lesson's own review
  const scopeKey = (sc) => `sd:${state.gid}${sc ? ":L" + sc : ""}`;
  const loadCards = (sc) => store.get(scopeKey(sc) + ":cards", {});
  const saveCards = (c, sc) => store.set(scopeKey(sc) + ":cards", c);

  function sentenceOf(para, form) {
    const text = para.t.map((t) => t[0]).join("");
    const parts = text.split(/(?<=[.;:?!])\s+/);
    const hit = parts.find((s) => s.toLowerCase().includes(form.toLowerCase())) || text;
    return hit.trim();
  }

  /* All cards for the lessons given, in lesson order. */
  async function buildDeck(lessons) {
    const cards = new Map();
    for (const l of lessons) {
      for (const tid of lessonTexts(l)) {
        const t = await load(`library/${tid}.json`);
        t.paras.forEach((p) => p.t.forEach((tok) => {
          if (tok.length < 2) return;
          const w = t.words[tok[1]];
          for (const h of w.heads || []) {
            const id = "m:" + h.lemma;
            if (!cards.has(id)) cards.set(id, { id, kind: "meaning", lesson: l.n, lemma: h.lemma, meaning: h.meaning, form: tok[0], ctx: w.ctx, line: sentenceOf(p, tok[0]), ref: t.ref, text: t.id });
          }
          if (w.parse) {
            const id = "p:" + w.form + "|" + w.label;
            if (!cards.has(id)) cards.set(id, { id, kind: "parse", wk: tok[1], lesson: l.n, lemma: w.lemma, form: tok[0], label: w.label, ctx: w.ctx, meaning: w.dpd, line: sentenceOf(p, tok[0]), ref: t.ref, text: t.id });
          }
        }));
      }
    }
    return [...cards.values()];
  }
  async function getDeck() {
    if (!state.deck) state.deck = await buildDeck(PREVIEW ? visibleLessons(state.group) : publishedLessons(state.group));
    return state.deck;
  }
  function learnedSet() {
    const c = loadCards(), out = new Set();
    for (const id in c) if (id.startsWith("m:") && c[id].s >= LEARNED_DAYS) out.add(id.slice(2));
    return out;
  }
  function dueInfo(deck, sc) {
    const c = loadCards(sc), now = Date.now();
    const due = deck.filter((k) => c[k.id] && c[k.id].due <= now);
    const fresh = deck.filter((k) => !c[k.id]);
    const today = new Date().toDateString();
    const nd = store.get(scopeKey(sc) + ":newday", { day: "", n: 0 });
    const newLeft = Math.max(0, NEW_PER_DAY - (nd.day === today ? nd.n : 0));
    return { due, fresh, newToday: fresh.slice(0, newLeft), total: due.length + Math.min(fresh.length, newLeft) };
  }

  /* ---------------- grammar links ---------------- */
  // term in a grammar label -> [section of Mor's grammar guide, text to point at inside it]
  const CASES = ["nominative", "accusative", "instrumental", "dative", "ablative", "genitive", "locative", "vocative"];
  const GRAMMAR_TERMS = [
    ...CASES.map((c) => [c, "cases", c[0].toUpperCase() + c.slice(1)]),
    ["future passive participle", "future-passive-participle"], ["present participle", "present-participle"],
    ["past participle", "past-participle"], ["present", "present"], ["imperative", "imperative"],
    ["optative", "optative"], ["future", "future"], ["aorist", "aorist"], ["absolutive", "absolutive"],
    ["infinitive", "infinitive"], ["sandhi", "sandhi"], ["compound", "compounds"], ["adjective", "adjectives"],
    ["pronoun", "pronouns"], ["verb", "verbs"],
  ].sort((x, y) => y[0].length - x[0].length);
  const GRAMMAR_RE = new RegExp("\\b(" + GRAMMAR_TERMS.map((t) => t[0]).join("|") + ")\\b", "g");
  // which kind of pronoun a word is, from its dictionary headword
  function pronounTopic(label, lemma) {
    const l = (lemma || "").toLowerCase();
    if (/\b(1st|2nd) person\b/.test(label)) return ["personal-pronouns"];
    if (/^(ima|ayaṃ|idaṃ)$/.test(l)) return ["demonstrative-pronouns"];
    if (/^(ya|yo|yaṃ)$/.test(l)) return ["relative-pronouns"];
    if (/^(ka|ko|kiṃ|katama|koci|kiñci)$/.test(l)) return ["interrogative-pronouns"];
    if (/^(ta|so|taṃ|eta|esa|eso)$/.test(l)) return ["personal-pronouns", "third-person pronoun"];
    return ["pronouns"];
  }
  let GRAMMAR_IDS = null;
  // src: where the word is ({lemma, t: text id, k: word key, pi: part index}), so a case
  // opens the declension table of that very word's type
  function linkGrammar(label, src) {
    const html = esc(label);
    const lemma = typeof src === "string" ? src : src?.lemma;
    if (GRAMMAR_IDS && !GRAMMAR_IDS.size) return html;
    return html.replace(GRAMMAR_RE, (m) => {
      if (CASES.includes(m) && src && src.t) {
        return `<a class="glink" href="#/${state.gid}/grammar/cases" data-case="${m}" data-t="${esc(src.t)}" data-k="${esc(src.k)}" data-pi="${src.pi ?? ""}">${m}</a>`;
      }
      let [, id, focus] = GRAMMAR_TERMS.find((t) => t[0] === m);
      if (id === "pronouns") [id, focus] = pronounTopic(label, lemma);
      if (GRAMMAR_IDS && !GRAMMAR_IDS.has(id)) return m;
      return `<a class="glink" href="#/${state.gid}/grammar/${id}" data-gram="${id}"${focus ? ` data-focus="${esc(focus)}"` : ""}>${m}</a>`;
    });
  }

  /* ---------------- header & footer ---------------- */
  function header(active, dueCount) {
    const g = state.group;
    const tab = (id, label, href, extra = "") => `<a href="${href}"${active === id ? ' aria-current="page"' : ""}>${label}${extra}</a>`;
    $("#top").innerHTML = `<div class="top-in">
      <div class="brandrow"><a class="brand" href="#/${g.id}"><b>Sutadhana</b><span>Pāḷi course</span></a>
        <button class="tourbtn" id="tourBtn" type="button"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="7 4 20 12 7 20 7 4"/></svg>Take a tour</button></div>
      <nav class="tabs" aria-label="Sections">
        ${tab("lessons", "Lessons", `#/${g.id}`)}
        ${tab("review", "Review", `#/${g.id}/review`, dueCount ? `<span class="due" aria-label="${dueCount} cards due">${dueCount}</span>` : "")}
        ${tab("grammar", "Grammar", `#/${g.id}/grammar`)}
        ${tab("library", "Library", `#/${g.id}/library`)}
      </nav></div>`;
  }
  async function headerWithDue(active) {
    header(active, 0);
    try { const d = dueInfo(await getDeck()); header(active, d.total); } catch (e) { /* ignore */ }
  }
  function footer() {
    $("#credit").innerHTML = `Word meanings from the <a href="https://www.dpdict.net" target="_blank" rel="noopener">Digital Pāḷi Dictionary</a> by Bodhirasa Bhikkhu, used under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>; grammar labels simplified and some meanings chosen to fit the passage. Translations are credited under each text. For participants of the course: please don't share this site outside the group.`;
  }
  const fmtDate = (iso) => iso ? new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "long", year: "numeric" }) : "";
  const fmtShort = (iso) => iso ? new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }) : "";

  /* lesson time: shown in UTC, with the viewer's local time on hover or tap */
  function utcLabel(hhmm) {
    const [h, m] = hhmm.split(":").map(Number);
    return `${h % 12 || 12}${m ? ":" + String(m).padStart(2, "0") : ""} ${h < 12 ? "am" : "pm"} UTC`;
  }
  function localTimeText(g) {
    try {
      const [h, m] = g.schedule.utc.split(":").map(Number);
      const wd = g.schedule.weekdays || [];          // 0 = Sunday … 6 = Saturday, in UTC
      const now = new Date();
      let next = null;
      for (let i = 0; i < 8 && !next; i++) {
        const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + i, h, m));
        if (wd.includes(d.getUTCDay()) && d > now) next = d;
      }
      if (!next) return "";
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      const time = next.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
      const sameDays = wd.every((x) => {
        const d = new Date(Date.UTC(2026, 0, 4 + x, h, m)); // 4 Jan 2026 is a Sunday
        return d.getDay() === x;
      });
      const day = next.toLocaleDateString([], { weekday: "long", day: "numeric", month: "long" });
      return `${time} in your time zone${tz ? " (" + tz.replace(/_/g, " ") + ")" : ""}.` +
        (sameDays ? "" : " For you this falls on a different day of the week.") +
        ` Next class: ${day}.`;
    } catch (e) { return ""; }
  }

  /* dāna card: three looks to choose from (settings.danaStyle a / b / c) */
  function danaCard(g, style) {
    if (!g.dana) return "";
    const text = `You may express your support and appreciation for the lessons by giving dāna, <span lang="pi" class="nowrap">yathā-pasādanaṃ</span>: according to your inspiration and ability. No act of generosity is too small, and it is always appreciated.`;
    const btn = (cls) => `<a class="btn ${cls}" href="${esc(g.dana)}" target="_blank" rel="noopener">Give dāna</a>`;
    if (style === "d") return `<div class="card dana dana-d"><div class="dana-top"><svg class="dana-ic" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8c4 5 6 10 6 15s-2 9-6 12c-4-3-6-7-6-12s2-10 6-15z"/><path d="M24 35c-6 0-12-3-16-9 5-1 10 0 14 3M24 35c6 0 12-3 16-9-5-1-10 0-14 3"/></svg><div class="dana-h">Dāna</div></div><p>You may express your support and appreciation for the lessons by giving dāna, <span lang="pi" class="nowrap">yathā-pasādanaṃ</span>: according to your inspiration and ability.</p>${btn("dana-btn-copper")}</div>`;
    if (style === "b") return `<div class="card dana dana-b"><div class="dana-h">Supporting the lessons</div><p>${text}</p>${btn("dana-btn-light")}</div>`;
    if (style === "c") return `<div class="card dana dana-c"><div class="dana-top"><svg class="dana-ic" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8c4 5 6 10 6 15s-2 9-6 12c-4-3-6-7-6-12s2-10 6-15z"/><path d="M24 35c-6 0-12-3-16-9 5-1 10 0 14 3M24 35c6 0 12-3 16-9-5-1-10 0-14 3"/></svg><div class="dana-h">Dāna</div></div><p>${text}</p>${btn("primary block")}</div>`;
    return `<div class="card dana dana-a"><div class="dana-h">Dāna</div><p>${text}</p>${btn("dana-btn-copper")}</div>`;
  }
  async function viewDanaOptions() {
    const g = state.group;
    await headerWithDue("lessons");
    const classes = `<div class="card"><div class="eyebrow">Classes</div><p style="margin:6px 0 0">${esc(g.schedule.days)}, ${esc(utcLabel(g.schedule.utc))}</p></div>`;
    $("#main").innerHTML = `<div class="head"><div class="eyebrow">For Mor only</div><h1>Dāna box versions</h1>
      <p class="sub">Each is shown as it would sit in the right-hand column, above the class times.</p></div>
      <div class="dana-opts">${["d", "a", "b", "c"].map((k, i) => `<div><h2>${i ? "Version " + i : "Combined version"}</h2><div class="side" style="display:flex;flex-direction:column;gap:14px">${danaCard(g, k)}${classes}</div></div>`).join("")}</div>`;
  }

  const DEMO_REC = "The recording of this lesson will be linked here after class.";

  /* ---------------- views ---------------- */
  async function viewGroup() {
    const g = state.group;
    const lessons = visibleLessons(g).slice().reverse();
    await headerWithDue("lessons");
    let deck = [], d = { total: 0 };
    try { deck = await getDeck(); d = dueInfo(deck); } catch (e) { /* ignore */ }
    const lib = await load("library/index.json");
    const titleOf = (id) => (lib.find((x) => x.id === id) || {}).titleEn || id;
    const play = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z"/></svg>`;
    const rows = lessons.map((l) => `
      <div class="lcard${l.published ? "" : " draft"}">
        <a class="lmain" href="#/${g.id}/lesson/${l.n}">
          <div class="num"><small>LESSON</small><b>${l.n}</b></div>
          <div class="t"><b>${esc(l.title || "Lesson " + l.n)}</b><span class="dt-m">${fmtShort(l.date)}</span><span>${esc(l.items.map((i) => i.text ? titleOf(i.text) : i.label || "").filter(Boolean).join(" · "))}</span></div>
          <div class="meta">${fmtShort(l.date)}${l.published ? "" : "<br>Draft (preview)"}</div>
          <div class="arr" aria-hidden="true">›</div></a>
        ${l.recording === "demo" ? `<button class="recbtn demo" data-note="${DEMO_REC}" data-label="Recording" aria-label="Recording of lesson ${l.n} (example)">${play}<span>Recording</span></button>`
          : l.recording ? `<a class="recbtn" href="${esc(l.recording)}" target="_blank" rel="noopener" aria-label="Recording of lesson ${l.n}">${play}<span>Recording</span></a>` : ""}
      </div>`).join("");
    const earlier = (g.earlier || []).length ? `
      <details class="earlier"><summary><span>Earlier lessons ${g.earlier[0].n}–${g.earlier[g.earlier.length - 1].n}: recordings</span></summary>
      <ul class="rec-list">${g.earlier.map((e) => `<li><a href="${esc(e.recording)}" target="_blank" rel="noopener"><span>${play} Lesson ${e.n}</span><span class="muted">${fmtShort(e.date)}</span></a></li>`).join("")}</ul></details>` : "";
    $("#main").innerHTML = `
      <div class="head"><div class="eyebrow">${esc(g.title)}</div><h1>Lessons</h1>
        <p class="sub">Each lesson holds the texts we read together, the recording and the new words.</p></div>
      <div class="cols">
        <div class="main">${rows || `<div class="notice">The first lesson in the app will appear here after class.</div>`}${earlier}</div>
        <aside class="side">
          <div class="card"><div class="eyebrow">Word review</div>
            <div class="big">${d.total}</div><div class="muted">${d.total === 1 ? "card" : "cards"} to review today</div>
            <a class="btn primary block" style="margin-top:14px" href="#/${g.id}/review">${d.total ? "Start review" : "Open review"}</a>
            <p class="muted" style="font-size:.85rem;margin:10px 0 0">Progress is saved on this device.</p></div>
          ${danaCard(g, g.settings?.danaStyle || "d")}
          <div class="card"><div class="eyebrow">Classes</div>
            <p style="margin:6px 0 0">${esc(g.schedule.days)}, <button class="timebtn" id="lessonTime" aria-describedby="pop">${esc(utcLabel(g.schedule.utc))}</button></p>
            ${g.materials ? `<p style="margin:10px 0 0"><a href="${esc(g.materials)}" target="_blank" rel="noopener">Course materials folder</a></p>` : ""}</div>
        </aside>
      </div>`;
    const tb = $("#lessonTime"), txt = localTimeText(g);
    if (tb && txt) {
      tb.dataset.note = txt; tb.dataset.label = "Your local time";
      tb.onmouseenter = () => showPop(tb); tb.onmouseleave = () => { if (!tb.dataset.pinned) hidePop(); };
      tb.onclick = (e) => { e.stopPropagation(); togglePop(tb); };
    } else if (tb) tb.classList.add("plain");
  }

  async function viewLesson(n) {
    const g = state.group;
    const l = g.lessons.find((x) => String(x.n) === String(n));
    await headerWithDue("lessons");
    if (!l || (!l.published && !PREVIEW)) { $("#main").innerHTML = `<a class="back" href="#/${g.id}"><span aria-hidden="true" style="color:var(--accent)">←</span> All lessons</a><div class="notice">This lesson isn't available yet.</div>`; return; }
    const lib = await load("library/index.json");
    const meta = (id) => lib.find((x) => x.id === id) || { id, titleEn: id };
    let k = 0;
    const items = l.items.map((i) => {
      k++;
      if (i.text) {
        const m = meta(i.text);
        return `<a class="row" href="#/${g.id}/read/${m.id}?lesson=${l.n}"><div class="dot">${k}</div>
          <div class="t"><b>${esc(m.title)}${m.titleEn ? ` <span class="muted" style="display:inline;font-size:1rem">· ${esc(m.titleEn)}</span>` : ""}</b><span>${esc(m.source)} · ${esc(m.ref)}${m.audio ? ` · <span class="has-audio">${HP_ICON}Audio</span>` : ""}</span></div><div class="arr" aria-hidden="true">›</div></a>`;
      }
      if (i.grammar) return `<a class="row" href="#/${g.id}/grammar/${esc(i.grammar)}"><div class="dot">${k}</div><div class="t"><b>${esc(i.label || i.grammar)}</b><span>Grammar guide</span></div><div class="arr" aria-hidden="true">›</div></a>`;
      return `<div class="row"><div class="dot">${k}</div><div class="t"><b>${esc(i.label)}</b>${i.detail ? `<span>${esc(i.detail)}</span>` : ""}</div></div>`;
    }).join("");

    // word list: headwords first met in this lesson vs. met in an earlier lesson
    const before = new Set();
    for (const pl of visibleLessons(g)) {
      if (pl.n >= l.n) break;
      for (const c of await buildDeck([pl])) if (c.kind === "meaning") before.add(c.lemma);
    }
    const lessonDeck = await buildDeck([l]);
    const lessonDue = dueInfo(lessonDeck, String(l.n)).total;
    const here = lessonDeck.filter((c) => c.kind === "meaning");
    const fresh = here.filter((c) => !before.has(c.lemma)), seen = here.filter((c) => before.has(c.lemma));
    const listHtml = (arr) => arr.length ? `<div class="wl">${arr.map((c) => `<div class="p">${esc(c.lemma)}</div><div class="m">${esc(c.meaning)}</div>`).join("")}</div>` : `<p class="muted">None.</p>`;

    $("#main").innerHTML = `
      <a class="back" href="#/${g.id}"><span aria-hidden="true" style="color:var(--accent)">←</span> All lessons</a>
      <div class="head"><div class="eyebrow">Lesson ${l.n}${l.date ? " · " + fmtDate(l.date) : ""}${l.published ? "" : " · draft"}</div>
        <h1>${esc(l.title || "Lesson " + l.n)}</h1></div>
      <div class="cols">
        <div class="main">
          ${l.recording === "demo" ? `<button class="btn recbtn-l demo" data-note="${DEMO_REC}" data-label="Recording" style="align-self:flex-start"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"/></svg>Watch the recording</button>` : ""}
          ${l.recording && l.recording !== "demo" ? `<a class="btn" href="${esc(l.recording)}" target="_blank" rel="noopener" style="align-self:flex-start"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"/></svg>Watch the recording</a>` : ""}
          <div class="eyebrow" style="margin-top:4px">What we read, in order</div>
          ${items}
          ${l.next ? `<div class="notice"><b style="font-weight:700">For next time:</b> ${esc(l.next)}</div>` : ""}
        </div>
        <aside class="side"><div class="card">
          ${l.published || PREVIEW ? `<a class="rvbtn" href="#/${g.id}/review?lesson=${l.n}">
            <span class="rv-ic" aria-hidden="true"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="6" width="13" height="15" rx="2"/><path d="M8 3h11a2 2 0 0 1 2 2v12"/></svg></span>
            <span class="rv-t"><b>Review vocabulary</b><small>from this lesson</small></span>
            ${lessonDue ? `<span class="rv-n" title="${lessonDue} cards ready">${lessonDue}</span>` : ""}
            <span class="rv-go" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></span></a>
          <p class="muted" style="font-size:.85rem;margin:8px 0 18px">Practise only this lesson’s words, with their own schedule.</p>` : ""}
          <div class="eyebrow">Words in this lesson</div>
          <div class="seg" role="group" aria-label="Word list">
            <button aria-pressed="true" data-wl="new">New · ${fresh.length}</button>
            <button aria-pressed="false" data-wl="seen">Seen before · ${seen.length}</button></div>
          <div id="wlNew">${listHtml(fresh)}</div><div id="wlSeen" hidden>${listHtml(seen)}</div>
          <p class="muted" style="font-size:.85rem;margin:10px 0 0">${l.published ? "These words are in your review." : "Words join the review when the lesson is published."}</p>
          <div class="two-btns"><a class="btn" href="#/${g.id}/glossary/${l.n}?print=1">Save glossary as PDF</a>
            <button class="btn" id="anki">Export to Anki</button></div>
        </div></aside>
      </div>`;
    $("#main").querySelectorAll("[data-wl]").forEach((b) => b.onclick = () => {
      $("#main").querySelectorAll("[data-wl]").forEach((x) => x.setAttribute("aria-pressed", x === b));
      $("#wlNew").hidden = b.dataset.wl !== "new"; $("#wlSeen").hidden = b.dataset.wl !== "seen";
    });
    $("#anki").onclick = () => exportAnki(here, `${g.id}-lesson-${l.n}`);
  }

  async function viewGlossary(n, autoPrint) {
    const g = state.group;
    const l = g.lessons.find((x) => String(x.n) === String(n));
    await headerWithDue("lessons");
    if (!l || (!l.published && !PREVIEW)) { $("#main").innerHTML = `<div class="notice">This lesson isn't available yet.</div>`; return; }
    const sections = [];
    for (const tid of lessonTexts(l)) {
      const t = await load(`library/${tid}.json`);
      const seen = new Set(), rows = [];
      t.paras.forEach((p) => p.t.forEach((tok) => {
        if (tok.length < 2 || seen.has(tok[1])) return;
        seen.add(tok[1]);
        const w = t.words[tok[1]];
        const meaning = w.ctx + (w.dpd && w.dpd !== w.ctx ? ` (DPD: ${w.dpd})` : "");
        const gram = w.label + (w.lemma && w.lemma.toLowerCase() !== tok[0].toLowerCase() ? `, from ${w.lemma}` : "");
        rows.push(`<tr><td lang="pi">${esc(tok[0].toLowerCase())}</td><td>${esc(gram)}</td><td>${esc(meaning)}</td></tr>`);
      }));
      sections.push(`<section class="gl-sec"><h2><span lang="pi">${esc(t.title)}</span> · ${esc(t.titleEn || "")}</h2>
        <p class="muted">${esc(t.source)} · ${esc(t.ref)}</p>
        <table class="gl"><thead><tr><th>Pāḷi</th><th>Grammar</th><th>Meaning</th></tr></thead><tbody>${rows.join("")}</tbody></table></section>`);
    }
    $("#main").innerHTML = `<div class="noprint"><a class="back" href="#/${g.id}/lesson/${l.n}"><span aria-hidden="true" style="color:var(--accent)">←</span> Back to Lesson ${l.n}</a>
        <p><button class="btn primary" id="doPrint">Save as PDF / print</button> <span class="muted" style="font-size:.9rem">In the print window, choose “Save as PDF”.</span></p></div>
      <div class="glossary"><div class="eyebrow">Sutadhana · Pāḷi course</div><h1>Lesson ${l.n} glossary</h1>
      <p class="sub">${esc(l.title || "")}${l.date ? " · " + fmtDate(l.date) : ""}</p>${sections.join("")}
      <p class="textcredit">Word meanings from the Digital Pāḷi Dictionary by Bodhirasa Bhikkhu (CC BY-NC-SA 4.0); grammar labels simplified.</p></div>`;
    $("#doPrint").onclick = () => window.print();
    if (autoPrint) setTimeout(() => window.print(), 400);
  }

  function exportAnki(cards, name) {
    const rows = cards.map((c) => [c.lemma, c.meaning, c.line ? c.line.replace(c.form, `<b>${c.form}</b>`) : "", c.ref || ""]
      .map((v) => String(v).replace(/\t|\n/g, " ")).join("\t"));
    const blob = new Blob(["#separator:tab\n#html:true\n#columns:Pāḷi\tMeaning\tExample\tSource\n" + rows.join("\n") + "\n"], { type: "text/tab-separated-values" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name + ".txt";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  /* ---------------- reader ---------------- */
  const myTr = (tid, pi) => store.get(`sd:mytr:${tid}:${pi}`, "") || "";
  const textScale = () => Number(store.get("sd:textscale", 1)) || 1;
  const hints = () => store.get("sd:hints", { subj: false, verb: false });
  // ---- Listening: Mor's reading of the text ----
  const PLAY_SVG = `<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="7 4 20 12 7 20 7 4"/></svg>`;
  const PAUSE_SVG = `<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>`;
  const SPEEDS = [1, 0.85, 0.7];
  const mmss = (x) => { x = Math.max(0, Math.round(x || 0)); return Math.floor(x / 60) + ":" + String(x % 60).padStart(2, "0"); };
  function getSpeed() { try { const v = parseFloat(localStorage.getItem("sd:speed")); return SPEEDS.includes(v) ? v : 1; } catch (e) { return 1; } }
  function stopAudio() { if (state.audio) { state.audio.pause(); state.audio = null; } }
  function listenBar(t) {
    return `<div class="listen" id="listen">
      <button class="lplay" id="lplay" aria-label="Play Mor’s reading">${PLAY_SVG}</button>
      <div class="lbody">
        <div class="ltop"><span class="ltitle">${HP_ICON}<span class="lt-long">Listen to Mor read this text</span><span class="lt-short">Mor’s reading</span></span><span class="ltime" id="ltime">0:00 / ${mmss(t.audioDur)}</span></div>
        <input type="range" class="lbar" id="lbar" min="0" max="${t.audioDur || 100}" step="0.5" value="0" aria-label="Position in the recording">
      </div>
      <button class="chip lspeed" id="lspeed" aria-label="Playback speed">${getSpeed()}×</button>
    </div>`;
  }
  function wireListen(t) {
    stopAudio();
    const a = new Audio(); a.preload = "none"; state.audio = a;
    let loaded = false, loading = false;
    const btn = $("#lplay"), bar = $("#lbar"), time = $("#ltime"), sp = $("#lspeed");
    const total = () => a.duration && isFinite(a.duration) ? a.duration : t.audioDur || 0;
    const paint = () => {
      bar.max = total(); if (!bar.matches(":active")) bar.value = a.currentTime;
      bar.style.setProperty("--fill", (total() ? a.currentTime / total() * 100 : 0) + "%");
      time.textContent = mmss(a.currentTime) + " / " + mmss(total());
    };
    const setBtn = () => { const on = !a.paused; btn.innerHTML = on ? PAUSE_SVG : PLAY_SVG;
      btn.setAttribute("aria-label", on ? "Pause" : "Play Mor’s reading"); $("#listen").classList.toggle("on", on); };
    // the whole file is fetched once (so it also works offline afterwards)
    async function ensure() {
      if (loaded || loading) return loaded;
      loading = true; btn.classList.add("busy");
      try {
        const res = await fetch(t.audio + "?v=" + state.dataVersion);
        if (!res.ok) throw new Error(res.status);
        a.src = URL.createObjectURL(await res.blob()); loaded = true;
      } catch (e) {
        time.textContent = "Can’t load the recording right now";
      }
      loading = false; btn.classList.remove("busy");
      return loaded;
    }
    a.playbackRate = getSpeed();
    btn.onclick = async () => {
      if (!a.paused) { a.pause(); return; }
      if (!(await ensure()) || state.audio !== a) return;
      a.playbackRate = getSpeed(); a.play().catch(() => {});
    };
    a.addEventListener("play", setBtn); a.addEventListener("pause", setBtn);
    a.addEventListener("ended", () => { a.currentTime = 0; setBtn(); paint(); });
    a.addEventListener("timeupdate", paint); a.addEventListener("loadedmetadata", paint);
    bar.oninput = async () => {
      const v = parseFloat(bar.value);
      bar.style.setProperty("--fill", (total() ? v / total() * 100 : 0) + "%");
      if (await ensure()) { a.currentTime = v; paint(); }
    };
    sp.onclick = () => {
      const next = SPEEDS[(SPEEDS.indexOf(getSpeed()) + 1) % SPEEDS.length];
      try { localStorage.setItem("sd:speed", next); } catch (e) {}
      a.playbackRate = next; sp.textContent = next + "×";
    };
  }

  async function viewReader(tid, lessonN) {
    const g = state.group;
    const t = await load(`library/${tid}.json`);
    await headerWithDue(lessonN ? "lessons" : "library");
    state.lastReader = location.hash;
    const notes = (g.notes || {})[tid] || [];
    const learned = learnedSet();
    const lesson = lessonN ? g.lessons.find((x) => String(x.n) === String(lessonN)) : null;
    const showHints = g.settings?.colourHints !== false;
    const markNew = g.settings?.markNewWords !== false;
    const h = hints();
    const isNew = (w) => (w.heads || []).some((x) => !learned.has(x.lemma));

    const boxes = t.paras.map((p, pi) => {
      const pnote = notes.find((n) => n.p === pi && !n.w);
      const toks = p.t.map((tok, ti) => {
        if (tok.length < 2) return `<span class="punct">${esc(tok[0])}</span>`;
        const w = t.words[tok[1]];
        const cls = ["w", w.role || "", isNew(w) ? "new" : ""].join(" ").trim();
        const wn = notes.find((n) => n.p === pi && n.w && n.w.toLowerCase() === tok[1]);
        return `<button class="${cls}" data-k="${esc(tok[1])}" data-p="${pi}" data-t="${ti}" lang="pi">${esc(tok[0])}</button>${wn ? `<button class="nmark" data-note="${esc(wn.text)}" aria-label="Teacher's note">i</button>` : ""}`;
      }).join("");
      return `<section class="box">
        ${pnote ? `<button class="nmark box-note" data-note="${esc(pnote.text)}" aria-label="Teacher's note">i</button>` : ""}
        <div class="box-no">${t.paras.length > 1 ? "Passage " + (pi + 1) : "Text"}</div>
        <div class="pali">${toks}</div>
        <div class="tgls">
          <button class="tgl" data-tr="${pi}" aria-expanded="false">Show translation</button>
          <button class="tgl" data-my="${pi}" aria-expanded="false">${myTr(tid, pi) ? "My translation ✓" : "My translation"}</button>
        </div>
        <div class="mytr" id="my${pi}" hidden>
          <label for="myta${pi}" class="sr">My translation of passage ${pi + 1}</label>
          <textarea id="myta${pi}" data-myta="${pi}" rows="3" placeholder="Write your own translation here…">${esc(myTr(tid, pi))}</textarea>
          <div class="mytr-st" id="myst${pi}">Saved on this device as you type.</div>
        </div>
        <div class="eng" id="tr${pi}" hidden>${esc(p.en)}</div></section>`;
    }).join("");

    // previous / next text within the lesson
    let prevNext = "";
    if (lesson) {
      const ids = lessonTexts(lesson), i = ids.indexOf(tid);
      const lib = await load("library/index.json");
      const nm = (id) => (lib.find((x) => x.id === id) || {}).title || id;
      prevNext = `<div class="nav-next">
        ${i > 0 ? `<a class="btn" href="#/${g.id}/read/${ids[i - 1]}?lesson=${lesson.n}">← <span lang="pi">${esc(nm(ids[i - 1]))}</span></a>` : "<span></span>"}
        ${i >= 0 && i < ids.length - 1 ? `<a class="btn primary" href="#/${g.id}/read/${ids[i + 1]}?lesson=${lesson.n}">Next: <span lang="pi">${esc(nm(ids[i + 1]))}</span> →</a>` : `<a class="btn" href="#/${g.id}/lesson/${lesson.n}">Back to lesson ${lesson.n}</a>`}
      </div>`;
    }

    $("#main").innerHTML = `
      <a class="back" href="${lesson ? `#/${g.id}/lesson/${lesson.n}` : `#/${g.id}/library`}"><span aria-hidden="true" style="color:var(--accent)">←</span> ${lesson ? "Back to Lesson " + lesson.n : "Back to the library"}</a>
      <div class="head"><div class="eyebrow">${esc(t.source)} · ${esc(t.ref)}</div>
        <h1 lang="pi">${esc(t.title)}</h1><p class="sub">${esc(t.titleEn || "")}</p></div>
      ${t.audio ? listenBar(t) : ""}
      <div class="toolbar">
        ${showHints ? `<span class="muted">Colour hints:</span>
        <button class="chip subj" data-hint="subj" aria-pressed="${h.subj}">Subject</button>
        <button class="chip verb" data-hint="verb" aria-pressed="${h.verb}">Verbs</button>` : ""}
        <span class="sizer" role="group" aria-label="Text size"><span class="muted">Text size:</span>
          <button class="chip" data-size="-1" aria-label="Smaller text">A−</button>
          <button class="chip" data-size="1" aria-label="Larger text">A+</button></span>
        ${markNew ? `<span class="legend"><span class="nw">word</span> not yet learned</span>` : ""}
      </div>
      ${t.intro ? `<p class="intro">${esc(t.intro)}</p>` : ""}
      <div id="text" style="--ps:${textScale()}" class="boxes${markNew ? " marknew" : ""}${h.subj ? " hint-subj" : ""}${h.verb ? " hint-verb" : ""}">${boxes}</div>
      <p class="muted" style="font-size:.9rem;margin:12px 0 0">Tap any word for its meaning and grammar.</p>
      ${prevNext}
      <p class="textcredit">${esc(t.credit || "")}</p>`;

    if (t.audio) wireListen(t);
    const box = $("#text");
    box.addEventListener("click", (e) => {
      const b = e.target.closest(".w");
      if (b) { openWord(t, b, notes); return; }
      const n = e.target.closest(".nmark");
      if (n) { togglePop(n); }
    });
    box.addEventListener("mouseover", (e) => { const n = e.target.closest(".nmark"); if (n) showPop(n); });
    box.addEventListener("mouseout", (e) => { const n = e.target.closest(".nmark"); if (n && !n.dataset.pinned) hidePop(); });
    $("#main").querySelectorAll("[data-tr]").forEach((b) => b.onclick = () => {
      const el = $("#tr" + b.dataset.tr), open = el.hidden;
      el.hidden = !open; b.textContent = open ? "Hide translation" : "Show translation"; b.setAttribute("aria-expanded", open);
    });
    $("#main").querySelectorAll("[data-my]").forEach((b) => b.onclick = () => {
      const el = $("#my" + b.dataset.my), open = el.hidden;
      el.hidden = !open; b.setAttribute("aria-expanded", open);
      if (open) $("#myta" + b.dataset.my).focus();
    });
    $("#main").querySelectorAll("[data-myta]").forEach((ta) => {
      let tm;
      ta.oninput = () => {
        clearTimeout(tm);
        tm = setTimeout(() => {
          const pi = ta.dataset.myta, v = ta.value;
          store.set(`sd:mytr:${tid}:${pi}`, v);
          $("#myst" + pi).textContent = "Saved on this device.";
          const btn = $(`[data-my="${pi}"]`); if (btn) btn.textContent = v.trim() ? "My translation ✓" : "My translation";
        }, 400);
      };
    });
    $("#main").querySelectorAll("[data-size]").forEach((b) => b.onclick = () => {
      const steps = [0.8, 0.9, 1, 1.1, 1.2, 1.35, 1.5];
      let i = steps.indexOf(textScale()); if (i < 0) i = 2;
      i = Math.max(0, Math.min(steps.length - 1, i + Number(b.dataset.size)));
      store.set("sd:textscale", steps[i]);
      box.style.setProperty("--ps", steps[i]);
    });
    $("#main").querySelectorAll("[data-hint]").forEach((b) => b.onclick = () => {
      const cur = hints(); cur[b.dataset.hint] = !cur[b.dataset.hint]; store.set("sd:hints", cur);
      b.setAttribute("aria-pressed", cur[b.dataset.hint]);
      box.classList.toggle("hint-" + b.dataset.hint, cur[b.dataset.hint]);
    });
  }

  /* teacher-note popover */
  const pop = () => $("#pop");
  function showPop(btn) {
    const p = pop();
    p.innerHTML = `<span class="lbl">${esc(btn.dataset.label || "Mor’s note")}</span>${esc(btn.dataset.note)}`;
    p.hidden = false;
    const r = btn.getBoundingClientRect(), pw = Math.min(320, innerWidth - 24);
    p.style.maxWidth = pw + "px";
    let left = Math.min(Math.max(12, r.left - 20), innerWidth - pw - 12);
    p.style.left = left + "px";
    const below = r.bottom + 8, ph = p.offsetHeight;
    p.style.top = (below + ph < innerHeight ? below : Math.max(8, r.top - ph - 8)) + "px";
  }
  function hidePop() { const p = pop(); p.hidden = true; document.querySelectorAll(".nmark[data-pinned]").forEach((b) => delete b.dataset.pinned); }
  function togglePop(btn) {
    if (btn.dataset.pinned) { hidePop(); return; }
    hidePop(); showPop(btn); btn.dataset.pinned = "1";
  }

  /* word sheet */
  function openWord(t, btn, notes) {
    document.querySelectorAll(".w.on").forEach((x) => x.classList.remove("on"));
    btn.classList.add("on");
    const w = t.words[btn.dataset.k];
    const wn = notes.find((n) => n.p === +btn.dataset.p && n.w && n.w.toLowerCase() === btn.dataset.k);
    const cards = loadCards();
    const learned = (w.heads || []).map((h) => cards["m:" + h.lemma]);
    const deckLine = !w.heads?.length ? "" : learned.every((c) => c && c.s >= LEARNED_DAYS) ? "Well learned" :
      learned.some((c) => c) ? `In your review${learned[0]?.due ? " · next review " + relDay(learned[0].due) : ""}` : "Not reviewed yet";
    const parts = w.parts ? `<ul class="parts">${w.parts.map((p, pi) => `<li><b lang="pi">${esc(p.form)}</b><span class="sep" aria-hidden="true">–</span><span class="gram">${linkGrammar(p.label, { lemma: p.lemma, t: t.id, k: btn.dataset.k, pi: pi })}</span><small>${esc(p.meaning)}${p.dpd && p.dpd !== p.meaning ? " · DPD: " + esc(p.dpd) : ""}</small></li>`).join("")}</ul>` : "";
    $("#sheetIn").innerHTML = `
      <div class="grab" aria-hidden="true"></div>
      <div class="s-head"><div style="flex:1;min-width:0">
          <div class="s-word" lang="pi">${esc(btn.textContent)}</div>
          ${w.lemma && w.lemma.toLowerCase() !== btn.textContent.toLowerCase() ? `<div class="s-lemma">from <b lang="pi">${esc(w.lemma)}</b></div>` : ""}</div>
        <span class="s-size" role="group" aria-label="Panel text size"><button class="icon" data-ssize="-1" aria-label="Smaller text">A−</button><button class="icon" data-ssize="1" aria-label="Larger text">A+</button></span>
        <button class="icon" id="sheetClose" aria-label="Close">×</button></div>
      <div class="rows">
        <div class="lbl">Grammar</div><div class="gram">${linkGrammar(w.label, { lemma: w.lemma, t: t.id, k: btn.dataset.k })}${/\p{L}-\p{L}/u.test(btn.textContent) && !/compound/.test(w.label) ? ` · ${linkGrammar("compound")}` : ""}</div>
        <div class="lbl">Here</div><div class="ctx">${esc(w.ctx)}</div>
        ${w.dpd ? `<div class="lbl">DPD</div><div>${esc(w.dpd)}${w.lit ? `<div class="lit">literally: ${esc(w.lit)}</div>` : ""}</div>` : ""}
        ${w.construction ? `<div class="lbl">Built from</div><div lang="pi">${esc(w.construction)}${w.root ? ` <span class="muted">(${esc(w.root)})</span>` : ""}</div>` : ""}
      </div>
      ${parts}
      ${w.note ? `<p class="note">${esc(w.note)}</p>` : ""}
      ${wn ? `<p class="tnote"><span class="lbl">Mor’s note</span>${esc(wn.text)}</p>` : ""}
      ${w.more?.length ? `<details class="more"><summary>Other meanings in the dictionary</summary><ul>${w.more.map((m) => `<li>${esc(m)}</li>`).join("")}</ul></details>` : ""}
      <div class="ext">
        <a href="https://www.dpdict.net/?q=${encodeURIComponent(w.lemma && !w.lemma.includes("+") ? (w.q || w.lemma) : btn.textContent.toLowerCase().replace(/[’'-]/g, ""))}" target="_blank" rel="noopener">Full dictionary entry ↗</a>
      </div>
      <div id="alsoIn"></div>
      ${deckLine ? `<div class="deckline">${deckLine}</div>` : ""}`;
    alsoFoundIn(t, w);
    const sh = $("#sheet");
    sh.hidden = false; document.body.classList.add("sheet-open");
    sh.scrollTop = 0;
    $("#sheetClose").onclick = closeSheet;
    sh.style.setProperty("--ss", sheetScale());
    sh.querySelectorAll("[data-ssize]").forEach((b) => b.onclick = () => {
      const steps = [0.85, 1, 1.15, 1.3, 1.5], i = steps.indexOf(sheetScale());
      const v = steps[Math.max(0, Math.min(steps.length - 1, i + +b.dataset.ssize))];
      try { localStorage.setItem("sd:sheetscale", v); } catch (e) {}
      sh.style.setProperty("--ss", v);
    });
    // keep the tapped word visible above the sheet on small screens
    {
      const r = btn.getBoundingClientRect(), limit = innerHeight * 0.5;
      if (r.bottom > limit) scrollBy({ top: r.bottom - limit + 20, behavior: "smooth" });
    }
  }
  async function alsoFoundIn(t, w) {
    const SKIP = new Set(["iti", "ti", "ca", "na", "vā", "pi", "kho", "hi", "eva", "api", "evaṃ"]);
    const heads = (w.heads || []).map((h) => h.lemma).filter((h) => !SKIP.has(h));
    if (!heads.length) return;
    let conc, lib;
    try { [conc, lib] = await Promise.all([load("library/concordance.json"), load("library/index.json")]); } catch (e) { return; }
    const box = $("#alsoIn"); if (!box) return;
    const g = state.group;
    const meta = (id) => lib.find((x) => x.id === id) || { id, title: id, titleEn: "" };
    const rows = heads.map((h) => {
      const ids = (conc[h] || []).filter((id) => id !== t.id);
      if (!ids.length) return "";
      const links = ids.map((id) => { const m = meta(id); return `<li><a href="#/${g.id}/read/${id}"><span lang="pi">${esc(m.title)}</span> · ${esc(m.titleEn)}</a> <span class="muted">${esc(m.ref || "")}</span></li>`; }).join("");
      const head = `<b lang="pi">${esc(h)}</b> is also found in ${ids.length} other ${ids.length === 1 ? "text" : "texts"}`;
      return ids.length <= 4 ? `<div class="also"><div>${head}:</div><ul>${links}</ul></div>`
        : `<details class="also"><summary>${head}</summary><ul>${links}</ul></details>`;
    }).join("");
    box.innerHTML = rows;
  }

  function sheetScale() { try { const v = parseFloat(localStorage.getItem("sd:sheetscale")); return [0.85, 1, 1.15, 1.3, 1.5].includes(v) ? v : 1; } catch (e) { return 1; } }
  function closeSheet() {
    $("#sheet").hidden = true; document.body.classList.remove("sheet-open");
    document.querySelectorAll(".w.on").forEach((x) => x.classList.remove("on"));
  }
  function relDay(ms) {
    const d = Math.round((ms - Date.now()) / DAY);
    return d <= 0 ? "today" : d === 1 ? "tomorrow" : `in ${d} days`;
  }

  /* grammar pop-up (opened from the word panel and review cards, so the reader stays open) */
  async function openGrammar(id, focus) {
    const gr = await load("grammar/index.json");
    const sec = gr.sections.find((x) => x.id === id);
    if (!sec) return;
    const chap = sec.chapter && sec.chapter !== sec.title ? sec.chapter : "Grammar guide";
    $("#gmBody").innerHTML = `<div class="eyebrow">${esc(chap)}</div><h2 id="gmTitle">${sec.titleHtml || esc(sec.title)}</h2>
      <div class="gram-body">${sec.html}</div>
      <div class="gm-foot"><a href="#/${state.gid}/grammar/${sec.id}" data-full="1">Open in the grammar guide →</a></div>`;
    const m = $("#gmodal"), box = $("#gmodal .gmodal-box");
    m.hidden = false; document.body.classList.add("modal-open");
    box.scrollTop = 0;
    requestAnimationFrame(() => m.classList.add("show"));
    $("#gmClose").focus({ preventScroll: true });
    if (focus) {
      const want = focus.toLowerCase();
      const cells = [...box.querySelectorAll(".gram-body td")];
      let el = cells.find((c) => c.textContent.trim().toLowerCase() === want);
      el = el ? el.closest("tr") : [...box.querySelectorAll(".gram-body p, .gram-body li")].find((x) => x.textContent.toLowerCase().includes(want));
      if (el) {
        el.classList.add("gfocus");
        setTimeout(() => {
          const top = el.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
          box.scrollTo({ top: Math.max(0, top - box.clientHeight / 3), behavior: "smooth" });
        }, 120);
      }
    }
  }
  // which cell of a declension table holds this case / number / gender / person
  function tableGrid(table) {
    const grid = [];
    [...table.rows].forEach((tr, r) => {
      grid[r] = grid[r] || [];
      let c = 0;
      [...tr.cells].forEach((td) => {
        while (grid[r][c]) c++;
        for (let i = 0; i < td.rowSpan; i++) for (let j = 0; j < td.colSpan; j++) {
          (grid[r + i] = grid[r + i] || [])[c + j] = td;
        }
        c += td.colSpan;
      });
    });
    return grid;
  }
  function findCell(table, caseName, number, gender, person) {
    const grid = tableGrid(table);
    const txt = (td) => (td ? td.textContent.trim().toLowerCase() : "");
    const r = grid.findIndex((row) => row.slice(0, 2).some((td) => txt(td) === caseName));
    if (r < 0) return null;
    const ncol = Math.max(...grid.map((row) => row.length));
    const heads = [];
    for (let c = 0; c < ncol; c++) heads[c] = grid.slice(0, r).map((row) => txt(row[c])).join(" ");
    const has = (c, w) => new RegExp("\\b" + w).test(heads[c]);
    const anyGender = heads.some((h) => /\b(masculine|neuter|feminine)/.test(h));
    const anyPerson = heads.some((h) => /\b(first|second) person/.test(h));
    let best = null;
    for (let c = 0; c < ncol; c++) {
      if (!has(c, number)) continue;
      if (gender && anyGender && !has(c, gender)) continue;
      if (person && anyPerson && !has(c, person)) continue;
      best = grid[r][c]; break;
    }
    return { row: grid[r][0].parentElement, cell: best };
  }
  async function openCase(ds) {
    const caseName = ds.case;
    const [gr, t] = await Promise.all([load("grammar/index.json"), load(`library/${ds.t}.json`)]);
    const w = t.words[ds.k];
    const x = ds.pi !== "" && ds.pi !== undefined && w.parts ? w.parts[+ds.pi] : w;
    if (!x) return openGrammar("cases", caseName[0].toUpperCase() + caseName.slice(1));
    const lab = x.label || "";
    const number = /\bplural\b/.test(lab) ? "plural" : "singular";
    const gender = (lab.match(/\b(masculine|neuter|feminine)\b/) || [])[1] || "";
    const person = /1st person/.test(lab) ? "first" : /2nd person/.test(lab) ? "second" : "";
    const Case = caseName[0].toUpperCase() + caseName.slice(1);
    let title, table, note = "", section = "cases";
    let P = x.para && gr.paradigms ? gr.paradigms[x.para] : null;
    if (P) {
      title = esc(P.title); table = P.html; section = P.section;
    } else if (x.decl) {
      title = `Declension of <span lang="pi">${esc(x.lemma)}</span>`; table = x.decl;
      note = `<p class="gm-src">Table from the Digital Pāḷi Dictionary.</p>`;
    } else return openGrammar("cases", Case);
    const def = (gr.caseDefs || {})[caseName];
    $("#gmBody").innerHTML = `<div class="eyebrow">${esc(Case)} ${esc(number)}${gender ? " · " + esc(gender) : ""}</div>
      <h2 id="gmTitle">${title}</h2>
      <p class="gm-like"><b lang="pi">${esc(x.form || w.form)}</b> is from <b lang="pi">${esc(x.lemma)}</b>${P ? ", which follows this pattern" : ""}.</p>
      ${def ? `<div class="gm-def"><b>${esc(Case)}:</b> ${def}</div>` : ""}
      <div class="gram-body" id="gmTable">${table}</div>${note}
      <div class="gm-foot">${section !== "cases" ? `<a href="#" data-gram="cases" data-focus="${esc(Case)}">The case system</a> · ` : ""}<a href="#/${state.gid}/grammar/${section}" data-full="1">Open in the grammar guide →</a></div>`;
    // the guide's ptp table has only nom. and acc.: "the rest is like anicca / gata"
    let tb = $("#gmTable table"), hit = tb && findCell(tb, caseName, number, gender, person);
    if (!hit && P && P.rest && gr.paradigms[P.rest]) {
      const R = gr.paradigms[P.rest];
      $("#gmTable").insertAdjacentHTML("beforeend", `<p class="gm-src">The rest of the declension is like that of ${esc(R.title.split(/\s+[–-]\s+/)[0])}:</p>${R.html}`);
      tb = $("#gmTable").querySelectorAll("table")[1];
      hit = findCell(tb, caseName, number, gender, person);
    }
    if (hit) { hit.row.classList.add("gfocus"); if (hit.cell) hit.cell.classList.add("gcell"); }
    const m = $("#gmodal"), box = $("#gmodal .gmodal-box");
    m.hidden = false; document.body.classList.add("modal-open");
    box.scrollTop = 0;
    requestAnimationFrame(() => m.classList.add("show"));
    $("#gmClose").focus({ preventScroll: true });
    if (hit) setTimeout(() => {
      const el = hit.row, top = el.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
      if (top > box.clientHeight * 0.7) box.scrollTo({ top: top - box.clientHeight / 3, behavior: "smooth" });
    }, 120);
  }
  function openTour() {
    closeSheet(); stopAudio();
    $("#gmBody").innerHTML = `<div class="eyebrow">Take a tour</div><h2 id="gmTitle">How the course app works</h2>
      <video class="tourvid" controls autoplay playsinline preload="metadata" poster="assets/tour-poster.jpg" src="assets/tour.mp4"></video>
      <p class="gm-src">About 4 minutes.</p>`;
    const m = $("#gmodal");
    m.hidden = false; document.body.classList.add("modal-open");
    requestAnimationFrame(() => m.classList.add("show"));
  }
  function closeGrammar() {
    const m = $("#gmodal");
    if (m.hidden) return false;
    m.querySelectorAll("video").forEach((v) => v.pause());
    m.classList.remove("show");
    document.body.classList.remove("modal-open");
    setTimeout(() => { if (!m.classList.contains("show")) m.hidden = true; }, 180);
    return true;
  }

  /* ---------------- review ---------------- */
  let session = null;
  async function viewReview(sc) {
    const g = state.group;
    sc = sc ? String(sc) : "";
    let deck;
    if (sc) {
      const l = g.lessons.find((x) => String(x.n) === sc);
      if (!l || (!l.published && !PREVIEW)) { location.replace(`#/${g.id}/review`); return; }
      deck = await buildDeck([l]);
      await headerWithDue("review");
    } else {
      deck = await getDeck();
    }
    const d = dueInfo(deck, sc);
    if (!sc) header("review", d.total);
    if (!session || session.gid !== g.id || session.sc !== sc) {
      const c = loadCards(sc);
      const queue = [...d.due.sort((a, b) => c[a.id].due - c[b.id].due), ...d.newToday];
      session = { gid: g.id, sc, queue, done: 0, start: queue.length, shown: false };
    }
    renderReview(deck);
  }
  function renderReview(deck) {
    const g = state.group;
    const s = session, sc = s.sc;
    const c = loadCards(sc);
    const backHref = sc ? `#/${g.id}/lesson/${sc}` : `#/${g.id}`, backTxt = sc ? `Lesson ${sc}` : "Lessons";
    const title = sc ? `Lesson ${sc} · words review` : "Word review";
    if (!s.queue.length) {
      const all = deck.length, seen = deck.filter((k) => c[k.id]).length;
      const learned = deck.filter((k) => c[k.id] && c[k.id].s >= LEARNED_DAYS).length;
      const nextDue = deck.map((k) => c[k.id]?.due).filter((x) => x > Date.now()).sort((a, b) => a - b)[0];
      $("#main").innerHTML = `<div class="rv">
        ${sc ? `<a class="back" href="${backHref}"><span aria-hidden="true" style="color:var(--accent)">←</span> Back to ${backTxt}</a>` : ""}
        <div class="head"><div class="eyebrow">${title}</div><h1>${s.start ? "Done for now" : "Nothing to review"}</h1>
          <p class="sub">${deck.length ? (nextDue ? "Next cards are due " + relDay(nextDue) + "." : "") : "Words appear here after each lesson is published."}</p></div>
        <div class="stats"><div><b>${s.done}</b><span>reviewed now</span></div><div><b>${seen}</b><span>cards started</span></div>
          <div><b>${learned}</b><span>well learned</span></div><div><b>${all}</b><span>cards in all</span></div></div>
        ${deck.length && !sc ? `<p><button class="linkbtn" id="ankiAll">Export all words to Anki</button></p>` : ""}
        <p class="muted" style="font-size:.9rem">${sc ? `This review has only the words of Lesson ${sc}, with its own schedule. The Review tab at the top mixes the words of all lessons.` : "Two kinds of card: the meaning of a word, and parsing a form as it appears in a text."} Progress is saved on this device only.</p></div>`;
      const ab = $("#ankiAll"); if (ab) ab.onclick = () => exportAnki(deck.filter((k) => k.kind === "meaning"), `${g.id}-all-words`);
      return;
    }
    const k = s.queue[0];
    const prev = FSRS.preview(c[k.id] || {});
    const line = esc(k.line).replace(new RegExp(esc(k.form).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), (m) => `<b>${m}</b>`);
    const front = k.kind === "meaning"
      ? `<div class="q-kind">What does it mean?</div><div class="q-word" lang="pi">${esc(k.lemma)}</div><div class="q-line" lang="pi">${line} · ${esc(k.ref)}</div>`
      : `<div class="q-kind">Parse this form</div><div class="q-word" lang="pi">${esc(k.form)}</div><div class="q-line" lang="pi">${line} · ${esc(k.ref)}</div>`;
    const back = k.kind === "meaning"
      ? `<div class="kv"><div class="lbl">Meaning</div><div style="font-size:1.2rem">${esc(k.meaning)}</div><div class="lbl">Here</div><div>${esc(k.ctx)}</div></div>`
      : `<div class="kv"><div class="lbl">From</div><div style="font-size:1.2rem" lang="pi">${esc(k.lemma)}</div><div class="lbl">Form</div><div class="gram" style="font-size:1.1rem">${linkGrammar(k.label, { lemma: k.lemma, t: k.text, k: k.wk })}</div><div class="lbl">Here</div><div>${esc(k.ctx)}</div></div>`;
    $("#main").innerHTML = `<div class="rv">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px"><a class="back" href="${backHref}"><span aria-hidden="true" style="color:var(--accent)">←</span> ${backTxt}</a>
        <span class="muted" style="font-size:.95rem">${sc ? `Lesson ${sc} · ` : ""}${s.done + 1} of ${s.start}${c[k.id] ? "" : " · new"}</span></div>
      <div class="progress"><i style="width:${Math.round(100 * s.done / Math.max(1, s.start))}%"></i></div>
      <div class="qcard">${front}
        <div class="q-ans" id="ans" ${s.shown ? "" : "hidden"}>${back}
          <div class="grades">
            ${["Again", "Hard", "Good", "Easy"].map((n, i) => `<button data-g="${i + 1}" class="${i === 2 ? "good" : ""}">${n}<small>${prev[i]}</small></button>`).join("")}
          </div></div>
        ${s.shown ? "" : `<button class="btn primary block" id="show" style="margin-top:22px">Show answer</button>`}
      </div></div>`;
    const sb = $("#show"); if (sb) { sb.onclick = () => { s.shown = true; renderReview(deck); }; sb.focus(); }
    $("#main").querySelectorAll("[data-g]").forEach((b) => b.onclick = () => grade(deck, +b.dataset.g));
  }
  function grade(deck, gr) {
    const s = session, sc = s.sc, k = s.queue.shift(), c = loadCards(sc);
    const wasNew = !c[k.id];
    c[k.id] = FSRS.review(c[k.id] || {}, gr);
    saveCards(c, sc);
    if (wasNew) {
      const today = new Date().toDateString(), key = scopeKey(sc) + ":newday";
      const nd = store.get(key, { day: "", n: 0 });
      store.set(key, { day: today, n: (nd.day === today ? nd.n : 0) + 1 });
    }
    if (gr === 1) s.queue.push(k); else s.done += 1;
    s.shown = false;
    renderReview(deck);
    window.scrollTo(0, 0);
  }

  /* ---------------- grammar ---------------- */
  async function viewGrammar(sid) {
    const g = state.group;
    const gr = await load("grammar/index.json");
    await headerWithDue("grammar");
    const secs = gr.sections;
    const i = Math.max(0, secs.findIndex((x) => x.id === sid));
    const sec = secs[i];
    // topics grouped by chapter
    const groups = [];
    secs.forEach((x) => {
      const c = x.chapter || x.title;
      let grp = groups.find((y) => y.c === c);
      if (!grp) groups.push(grp = { c, items: [] });
      grp.items.push(x);
    });
    const link = (x, cls, label) => `<a class="${cls}" href="#/${g.id}/grammar/${x.id}"${x.id === sec.id ? ' aria-current="page"' : ""}>${esc(label || x.title)}</a>`;
    const nav = groups.map((grp) => grp.items.length === 1 && grp.items[0].title === grp.c ? link(grp.items[0], "gn-top")
      : `<div class="gn-ch">${esc(grp.c)}</div>${grp.items.map((x) => x.title === grp.c ? link(x, "gn-sub", "Introduction") : link(x, "gn-sub")).join("")}`).join("");
    const prev = secs[i - 1], next = secs[i + 1];
    const backTo = state.lastReader ? `<a class="back" href="${esc(state.lastReader)}"><span aria-hidden="true" style="color:var(--accent)">←</span> Back to the text</a>` : "";
    const chap = sec.chapter && sec.chapter !== sec.title ? sec.chapter : gr.title;
    $("#main").innerHTML = `${backTo}
      <div class="gram-layout">
        <details class="gram-nav" id="gnav"${innerWidth > 860 || !sid ? " open" : ""}><summary>All topics</summary><nav aria-label="Grammar topics">${nav}</nav></details>
        <article class="gram-main" id="gmain" style="--gs:${gramScale()}">
          <div class="head"><div class="eyebrow">${esc(chap)}</div><h1>${sec.titleHtml || esc(sec.title)}</h1></div>
          <div class="toolbar"><span class="sizer" role="group" aria-label="Text size"><span class="muted">Text size:</span>
            <button class="chip" data-gsize="-1" aria-label="Smaller text">A−</button>
            <button class="chip" data-gsize="1" aria-label="Larger text">A+</button></span></div>
          <div class="gram-body">${sec.html}</div>
          <div class="nav-next">
            ${prev ? `<a class="btn" href="#/${g.id}/grammar/${prev.id}">← ${esc(prev.title)}</a>` : "<span></span>"}
            ${next ? `<a class="btn primary" href="#/${g.id}/grammar/${next.id}">${esc(next.title)} →</a>` : "<span></span>"}
          </div>
          <p class="textcredit">${esc(gr.title)} · ${esc(gr.author || "")}</p>
        </article>
      </div>`;
    closeSheet();
    $("#main").querySelectorAll("[data-gsize]").forEach((b) => b.onclick = () => {
      const steps = [0.9, 1, 1.1, 1.2, 1.35], cur = gramScale();
      const i2 = Math.max(0, Math.min(steps.length - 1, steps.indexOf(cur) + +b.dataset.gsize));
      try { localStorage.setItem("sd:gscale", steps[i2]); } catch (e) {}
      $("#gmain").style.setProperty("--gs", steps[i2]);
    });
    // practice sentences: a box beside each one for the student's own translation
    if (sec.id === "practicing-cases") {
      $("#main").querySelectorAll(".gram-body table.t-practice").forEach((tb, ti) => {
        [...tb.rows].forEach((tr, ri) => {
          const key = `sd:gp:${ti}-${ri}`;
          let v = ""; try { v = localStorage.getItem(key) || ""; } catch (e) {}
          const td = document.createElement("td");
          td.className = "gp";
          td.innerHTML = `<textarea rows="1" aria-label="Your translation" placeholder="Your translation…">${esc(v)}</textarea>`;
          const ta = td.firstChild;
          const fit = () => { ta.style.height = "auto"; ta.style.height = ta.scrollHeight + "px"; };
          ta.addEventListener("input", () => { try { localStorage.setItem(key, ta.value); } catch (e) {} fit(); });
          tr.appendChild(td); requestAnimationFrame(fit);
        });
      });
      $("#main").querySelector(".gram-body").insertAdjacentHTML("afterbegin", `<p class="gp-note">Write your translation next to each sentence. It’s saved on this device.</p>`);
    }
    if (sid) window.scrollTo(0, 0);
  }
  function gramScale() { try { const v = parseFloat(localStorage.getItem("sd:gscale")); return [0.9, 1, 1.1, 1.2, 1.35].includes(v) ? v : 1; } catch (e) { return 1; } }

  /* ---------------- library ---------------- */
  async function viewLibrary() {
    const g = state.group;
    const lib = await load("library/index.json");
    await headerWithDue("library");
    const books = [];
    lib.forEach((x) => {
      const key = x.bookLesson ? `Lesson ${x.bookLesson}` : "Other texts";
      let b = books.find((y) => y.key === key);
      if (!b) books.push(b = { key, initial: [], further: [], extra: [] });
      b[x.section || "extra"].push(x);
    });
    const row = (x) => `<a class="row" href="#/${g.id}/read/${x.id}"><div class="t"><b lang="pi">${esc(x.title)} <span class="muted" style="display:inline;font-size:1rem">· ${esc(x.titleEn)}</span></b><span>${esc(x.ref)}${x.audio ? ` · <span class="has-audio">${HP_ICON}Audio</span>` : ""}</span></div><div class="arr" aria-hidden="true">›</div></a>`;
    const part = (title, arr) => arr.length ? `<div class="eyebrow" style="margin:14px 0 8px">${title}</div><div class="boxes" style="gap:10px">${arr.map(row).join("")}</div>` : "";
    $("#main").innerHTML = `<div class="head"><div class="eyebrow">A New Course in Reading Pāḷi, and more</div><h1>Library</h1>
      <p class="sub">Every text prepared for the course, including ones we haven't read in class yet.</p></div>
      ${books.map((b) => `<section style="margin-top:22px"><h2>${esc(b.key)}</h2>
        ${part("Initial readings", b.initial)}${part("Further readings", b.further)}${part("Extra readings", b.extra)}</section>`).join("")}`;
  }

  /* ---------------- router ---------------- */
  async function route() {
    closeSheet(); hidePop(); closeGrammar(); stopAudio();
    document.body.classList.toggle("wide", /\/grammar(\/|$)/.test(location.hash));
    const [path, query] = location.hash.replace(/^#\/?/, "").split("?");
    const parts = path.split("/").filter(Boolean);
    const q = new URLSearchParams(query || "");
    try {
      const idx = await load("groups/index.json");
      state.dataVersion = idx.version || "";
      if (!GRAMMAR_IDS) { try { GRAMMAR_IDS = new Set((await load("grammar/index.json")).sections.map((x) => x.id)); } catch (e) { GRAMMAR_IDS = new Set(); } }
      if (!parts.length) { location.replace(`#/${idx.current}`); return; }
      const gid = parts[0];
      if (!idx.groups.some((x) => x.id === gid)) { $("#main").innerHTML = `<div class="notice">This group page doesn't exist. <a href="#/${idx.current}">Go to the current group</a>.</div>`; return; }
      await getGroup(gid);
      document.title = "Sutadhana · Pāḷi course";
      const v = parts[1];
      if (!v) await viewGroup();
      else if (v === "lesson") await viewLesson(parts[2]);
      else if (v === "read") await viewReader(parts[2], q.get("lesson"));
      else if (v === "review") await viewReview(q.get("lesson"));
      else if (v === "grammar") await viewGrammar(parts[2]);
      else if (v === "library") await viewLibrary();
      else if (v === "glossary") await viewGlossary(parts[2], q.get("print") === "1");
      else if (v === "dana-options" && PREVIEW) await viewDanaOptions();
      else await viewGroup();
      if (v !== "review") session = null;
      footer();
      if (!/read|grammar/.test(v || "")) window.scrollTo(0, 0);
      else if (v === "read") window.scrollTo(0, 0);
      $("#main").focus({ preventScroll: true });
    } catch (e) {
      console.error(e);
      $("#main").innerHTML = `<div class="notice">Something didn't load. Please check your connection and reload the page.</div>`;
    }
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { if (closeGrammar()) return; if (!$("#sheet").hidden) closeSheet(); hidePop(); }
  });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-gram], a[data-case]");
    if (a && a.closest("#sheet, .qcard, #gmodal") && a.dataset.case) { e.preventDefault(); openCase(a.dataset); return; }
    if (a && a.closest("#sheet, .qcard, #gmodal")) { e.preventDefault(); openGrammar(a.dataset.gram, a.dataset.focus); return; }
    if (e.target.closest("a[data-full]")) { closeGrammar(); closeSheet(); return; }
    if (e.target.id === "gmodal" || e.target.closest("#gmClose")) closeGrammar();
  });
  document.addEventListener("click", (e) => {
    const demo = e.target.closest("button.demo");
    if (demo) { e.stopPropagation(); togglePop(demo); return; }
    if (!e.target.closest(".nmark") && !e.target.closest("#pop") && !e.target.closest(".timebtn")) hidePop();
  });
  document.addEventListener("click", (e) => { if (e.target.closest("#tourBtn")) openTour(); });

  /* phones only: a small button to save the app to the home screen, with instructions */
  {
    const ua = navigator.userAgent;
    const isIOS = /iPhone|iPod/.test(ua) || (/iPad|Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    const isAndroid = /Android/.test(ua);
    const isPhone = (isIOS || isAndroid || /Mobi/.test(ua)) && matchMedia("(pointer:coarse)").matches;
    const installed = matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
    let dismissed = false; try { dismissed = localStorage.getItem("sd:a2hs") === "no"; } catch (e) {}
    let deferred = null;
    addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); deferred = e; });
    if (isPhone && !installed && !dismissed) {
      const bar = document.createElement("div");
      bar.className = "a2hs";
      bar.innerHTML = `<button class="a2hs-go" type="button"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M12 7v7M8.5 10.5 12 14l3.5-3.5"/></svg>Save this app to your home screen</button><button class="a2hs-x" type="button" aria-label="Hide">×</button>`;
      document.body.appendChild(bar);
      document.body.classList.add("has-a2hs");
      bar.querySelector(".a2hs-x").onclick = () => {
        bar.remove(); document.body.classList.remove("has-a2hs");
        try { localStorage.setItem("sd:a2hs", "no"); } catch (e) {}
      };
      bar.querySelector(".a2hs-go").onclick = () => {
        const shareIc = `<svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-label="Share"><path d="M12 3v12M7.5 7.5 12 3l4.5 4.5"/><path d="M6 11H5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1h-1"/></svg>`;
        const dots = `<b class="ic" aria-label="menu">⋮</b>`;
        const ios = `<section class="a2-sec"><h3>iPhone</h3><ol>
            <li>Open this page in <b>Safari</b>.</li>
            <li>Tap the <b>Share</b> button ${shareIc}. It’s at the bottom of the screen, or on newer iPhones inside the <b>•••</b> menu.</li>
            <li>Scroll down and tap <b>Add to Home Screen</b>.</li>
            <li>Tap <b>Add</b>, at the top right.</li></ol></section>`;
        const and = `<section class="a2-sec"><h3>Android</h3>
            ${deferred ? `<button class="btn primary" id="a2Install" type="button" style="margin:2px 0 10px">Add it now</button><p class="muted" style="margin:0 0 6px">Or do it yourself:</p>` : ""}<ol>
            <li>Open this page in <b>Chrome</b>.</li>
            <li>Tap the menu ${dots} at the top right.</li>
            <li>Tap <b>Add to Home screen</b> (on some phones: <b>Install app</b>).</li>
            <li>Tap <b>Add</b> (or <b>Install</b>).</li></ol></section>`;
        $("#gmBody").innerHTML = `<div class="eyebrow">On your phone</div><h2 id="gmTitle">Save the app to your home screen</h2>
          <p style="margin:0 0 12px">Then it opens like any other app, with its own icon.</p>
          <div class="a2-grid">${isAndroid ? and + ios : ios + and}</div>`;
        const m = $("#gmodal");
        m.hidden = false; document.body.classList.add("modal-open");
        requestAnimationFrame(() => m.classList.add("show"));
        const ib = $("#a2Install");
        if (ib) ib.onclick = async () => { deferred.prompt(); try { await deferred.userChoice; } catch (e) {} deferred = null; closeGrammar(); };
      };
    }
  }
  // word panel: a tap anywhere outside it closes it (a tap on another word just switches)
  document.addEventListener("click", (e) => {
    if ($("#sheet").hidden) return;
    if (e.target.closest("#sheet, .w, #gmodal, #pop, .nmark")) return;
    closeSheet();
  });
  // ...and on touch screens it can be dragged down
  {
    const sh = $("#sheet");
    let y0 = null, dy = 0;
    sh.addEventListener("touchstart", (e) => {
      if (sh.scrollTop > 0 && !e.target.closest(".grab, .s-head")) { y0 = null; return; }
      y0 = e.touches[0].clientY; dy = 0; sh.style.transition = "none";
    }, { passive: true });
    sh.addEventListener("touchmove", (e) => {
      if (y0 === null) return;
      dy = e.touches[0].clientY - y0;
      if (dy > 0) { sh.style.transform = `translateY(${dy}px)`; if (e.cancelable) e.preventDefault(); }
    }, { passive: false });
    sh.addEventListener("touchend", () => {
      if (y0 === null) return;
      sh.style.transition = "";
      if (dy > 70) {
        sh.style.transform = "translateY(100%)";
        setTimeout(() => { closeSheet(); sh.style.transform = ""; }, 200);
      } else sh.style.transform = "";
      y0 = null;
    });
  }
  addEventListener("hashchange", route);
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
    navigator.serviceWorker.register("sw.js").then(() => navigator.serviceWorker.ready).then(async () => {
      try {   // keep every text available offline
        const lib = await load("library/index.json");
        await Promise.all([load("library/concordance.json"), load("grammar/index.json"), ...lib.map((x) => load(`library/${x.id}.json`))]);
      } catch (e) { /* offline or blocked: fine */ }
    }).catch(() => {});
  }
  route();
})();
