/* Spaced repetition scheduler: FSRS-5 with its published default parameters
   (the algorithm Anki uses). Ratings: 1 Again, 2 Hard, 3 Good, 4 Easy.
   A card is {s: stability (days), d: difficulty 1–10, due: ms, last: ms, reps, lapses}. */
(function () {
  "use strict";
  const W = [0.40255, 1.18385, 3.173, 15.69105, 7.1949, 0.5345, 1.4604, 0.0046, 1.54575,
    0.1192, 1.01925, 1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898, 0.51655, 0.6621];
  const DECAY = -0.5, FACTOR = 19 / 81, RETENTION = 0.9, MAX_IVL = 3650;
  const DAY = 86400000, MIN = 60000;

  const clampD = (d) => Math.min(10, Math.max(1, d));
  const initS = (g) => Math.max(W[g - 1], 0.1);
  const initD = (g) => clampD(W[4] - Math.exp(W[5] * (g - 1)) + 1);
  const retr = (t, s) => Math.pow(1 + FACTOR * t / s, DECAY);
  const ivl = (s) => Math.min(MAX_IVL, Math.max(1, Math.round(s / FACTOR * (Math.pow(RETENTION, 1 / DECAY) - 1))));

  function nextD(d, g) {
    const delta = -W[6] * (g - 3);
    const d1 = d + delta * (10 - d) / 9;
    return clampD(W[7] * initD(4) + (1 - W[7]) * d1);
  }
  function recallS(d, s, r, g) {
    const hard = g === 2 ? W[15] : 1, easy = g === 4 ? W[16] : 1;
    return s * (1 + Math.exp(W[8]) * (11 - d) * Math.pow(s, -W[9]) * (Math.exp((1 - r) * W[10]) - 1) * hard * easy);
  }
  function forgetS(d, s, r) {
    const f = W[11] * Math.pow(d, -W[12]) * (Math.pow(s + 1, W[13]) - 1) * Math.exp((1 - r) * W[14]);
    return Math.min(f, s);
  }
  function shortS(s, g) { return s * Math.exp(W[17] * (g - 3 + W[18])); }

  /* Returns the updated card after rating g at time now. */
  function review(card, g, now) {
    now = now || Date.now();
    const c = Object.assign({ reps: 0, lapses: 0 }, card);
    if (!c.s) {                     // new card
      c.s = initS(g); c.d = initD(g);
    } else {
      const elapsed = Math.max(0, (now - c.last) / DAY);
      if (elapsed < 1) {            // reviewed again the same day
        c.s = shortS(c.s, g);
      } else {
        const r = retr(elapsed, c.s);
        c.s = g === 1 ? forgetS(c.d, c.s, r) : recallS(c.d, c.s, r, g);
      }
      c.d = nextD(c.d, g);
    }
    c.reps += 1;
    if (g === 1) { c.lapses += 1; c.due = now + 10 * MIN; }
    else c.due = now + ivl(c.s) * DAY;
    c.last = now;
    return c;
  }

  /* Human label for what each rating would schedule. */
  function preview(card, now) {
    now = now || Date.now();
    return [1, 2, 3, 4].map((g) => {
      const n = review(card, g, now);
      const ms = n.due - now;
      if (ms < DAY) return Math.round(ms / MIN) + " min";
      const days = Math.round(ms / DAY);
      if (days < 31) return days + (days === 1 ? " day" : " days");
      if (days < 365) return Math.round(days / 30) + " mo";
      return (days / 365).toFixed(1) + " yr";
    });
  }

  window.FSRS = { review, preview, DAY };
})();
