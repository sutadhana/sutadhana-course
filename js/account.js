/* Optional accounts: sign in with Google or an emailed link, and keep review progress,
   own translations and settings in the student's account so they follow them to any device.
   Without signing in everything keeps working on the one device, as before. */
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getAuth, onAuthStateChanged, GoogleAuthProvider, signInWithPopup, signInWithRedirect, getRedirectResult,
  sendSignInLinkToEmail, isSignInWithEmailLink, signInWithEmailLink, signOut,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, getDoc, setDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const app = initializeApp({
  apiKey: "AIzaSyBAu6MDsABBSFzXErsd2cjEMkRO-jyYW5o",
  authDomain: "suta-dhana.firebaseapp.com",
  projectId: "suta-dhana",
  storageBucket: "suta-dhana.firebasestorage.app",
  messagingSenderId: "835596158374",
  appId: "1:835596158374:web:64c8cec32920eb1e9bbb67",
});
const auth = getAuth(app);
const db = getFirestore(app);

const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const EMAIL_KEY = "sdacct:email", TIMES_KEY = "sdacct:times";
// what travels with the account: everything the app keeps under "sd:", except the install hint
const synced = (k) => k && k.startsWith("sd:") && k !== "sd:a2hs";

let user = null, applying = false, pushTimer = null, dirty = {};
const ls = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { rawSet.call(localStorage, k, v); } catch (e) {} },
  keys() { try { return Object.keys(localStorage); } catch (e) { return []; } },
};
const times = () => { try { return JSON.parse(ls.get(TIMES_KEY) || "{}"); } catch (e) { return {}; } };

/* note every change the app makes, so it can be sent to the account */
const rawSet = Storage.prototype.setItem;
Storage.prototype.setItem = function (k, v) {
  rawSet.call(this, k, v);
  if (this !== window.localStorage || applying || !synced(k)) return;
  const t = times(); t[k] = Date.now(); ls.set(TIMES_KEY, JSON.stringify(t));
  if (user) { dirty[k] = { v: String(v), t: t[k] }; schedulePush(); }
};

function schedulePush() { clearTimeout(pushTimer); pushTimer = setTimeout(push, 1500); }
async function push() {
  if (!user || !Object.keys(dirty).length) return;
  const batch = dirty; dirty = {};
  try { await setDoc(doc(db, "users", user.uid), { data: batch, updated: Date.now() }, { merge: true }); }
  catch (e) { Object.assign(dirty, batch, dirty); setStatus("Couldn't save to your account just now; it will try again."); }
}
addEventListener("pagehide", push);
addEventListener("online", push);

/* review cards: keep, card by card, the one reviewed most recently */
function mergeCards(a, b) {
  let x = {}, y = {};
  try { x = JSON.parse(a || "{}"); } catch (e) {}
  try { y = JSON.parse(b || "{}"); } catch (e) {}
  const out = { ...x };
  for (const [id, c] of Object.entries(y)) if (!out[id] || (c && (c.last || 0) > (out[id].last || 0))) out[id] = c;
  return JSON.stringify(out);
}

/* first sign-in on a device: combine what is here with what the account already holds */
async function sync() {
  setStatus("Syncing…");
  const snap = await getDoc(doc(db, "users", user.uid));
  const cloud = (snap.exists() && snap.data().data) || {};
  const t = times(), up = {};
  const keys = new Set([...ls.keys().filter(synced), ...Object.keys(cloud)]);
  applying = true;
  for (const k of keys) {
    const local = ls.get(k), c = cloud[k];
    const lt = t[k] || 0;
    let v;
    if (c == null) v = local;
    else if (local == null) v = c.v;
    else if (k.endsWith(":cards")) v = mergeCards(local, c.v);
    else v = (c.t || 0) >= lt ? c.v : local;
    if (v == null) continue;
    if (v !== local) ls.set(k, v);
    const nt = Math.max(lt, (c && c.t) || 0) || Date.now();
    t[k] = nt;
    if (!c || c.v !== v) up[k] = { v, t: nt };
  }
  applying = false;
  ls.set(TIMES_KEY, JSON.stringify(t));
  if (Object.keys(up).length) await setDoc(doc(db, "users", user.uid), { data: up, updated: Date.now() }, { merge: true });
  setStatus("");
  dispatchEvent(new HashChangeEvent("hashchange"));   // redraw with the combined progress
}

/* ---------------- header button and sign-in window ---------------- */
const ICON = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>`;
const G_ICON = `<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>`;

function renderButton() {
  const row = $("#top .brandrow");
  if (!row || $("#acctBtn", row)) return;
  const b = document.createElement("button");
  b.id = "acctBtn"; b.type = "button"; b.className = "tourbtn acctbtn";
  b.innerHTML = user ? `${ICON}<span>Account</span>` : `${ICON}<span>Sign in</span>`;
  b.setAttribute("aria-label", user ? "Your account" : "Sign in to save your progress");
  b.onclick = openWin;
  let wrap = $(".topbtns", row);
  if (!wrap) {
    wrap = document.createElement("div"); wrap.className = "topbtns";
    const tour = $("#tourBtn", row);
    if (tour) { tour.replaceWith(wrap); wrap.append(tour); } else row.append(wrap);
  }
  wrap.prepend(b);
}
new MutationObserver(renderButton).observe($("#top"), { childList: true, subtree: true });
const refreshButton = () => { $("#acctBtn")?.remove(); renderButton(); };

let win;
function openWin(mode) {
  if (!win) {
    win = document.createElement("div");
    win.className = "gmodal acct"; win.hidden = true;
    win.innerHTML = `<div class="gmodal-box" role="dialog" aria-modal="true" aria-labelledby="acTitle"><button class="icon gm-x" aria-label="Close">×</button><div class="ac-body"></div></div>`;
    document.body.append(win);
    win.addEventListener("click", (e) => { if (e.target === win || e.target.closest(".gm-x")) closeWin(); });
    addEventListener("keydown", (e) => { if (e.key === "Escape" && !win.hidden) closeWin(); });
  }
  const body = $(".ac-body", win);
  if (mode === "confirm") {
    body.innerHTML = `<h2 id="acTitle">Finish signing in</h2>
      <p>You opened the sign-in link on a different device or browser. Please type your email address once more.</p>
      <form class="ac-form" id="acConfirm"><label class="sr" for="acEm2">Email</label>
        <input id="acEm2" type="email" required autocomplete="email" placeholder="you@example.com">
        <button class="btn primary" type="submit">Sign in</button></form>
      <p class="ac-st" id="acSt" role="status"></p>`;
    $("#acConfirm").onsubmit = (e) => { e.preventDefault(); finishEmail($("#acEm2").value.trim()); };
  } else if (user) {
    body.innerHTML = `<h2 id="acTitle">Your account</h2>
      <p>Signed in as <b>${esc(user.email || user.displayName || "")}</b>.</p>
      <p>Your review progress, your own translations and your settings are saved to your account, so they follow you to any phone or computer where you sign in.</p>
      <p class="ac-st" id="acSt" role="status"></p>
      <button class="btn" id="acOut" type="button">Sign out</button>
      <p class="ac-small">Signing out keeps a copy of your progress on this device.</p>`;
    $("#acOut").onclick = async () => { await push(); await signOut(auth); closeWin(); };
  } else {
    body.innerHTML = `<h2 id="acTitle">Save your progress</h2>
      <p>Sign in to keep your review progress, your own translations and your settings in your account, and use them on any phone or computer. It's optional: without signing in, everything is kept on this device only.</p>
      <button class="btn ac-google" id="acG" type="button">${G_ICON}<span>Continue with Google</span></button>
      <div class="ac-or"><span>or</span></div>
      <form class="ac-form" id="acMail"><label for="acEm">Email me a sign-in link (no password)</label>
        <input id="acEm" type="email" required autocomplete="email" placeholder="you@example.com">
        <button class="btn primary" type="submit">Send link</button></form>
      <p class="ac-st" id="acSt" role="status"></p>
      <button class="btn ac-later" type="button" id="acLater">Not now</button>
      <p class="ac-small">Privacy: we keep only your email address and your progress in this course, stored with Google Firebase. They are used for nothing else and never shared. To have your account deleted, write to Mor.</p>`;
    $("#acLater").onclick = closeWin;
    $("#acG").onclick = google;
    $("#acMail").onsubmit = (e) => { e.preventDefault(); sendLink($("#acEm").value.trim()); };
  }
  win.hidden = false;
  requestAnimationFrame(() => win.classList.add("show"));
  ($("input", body) || $("button.btn", body))?.focus();
}
function closeWin() { if (win) { win.classList.remove("show"); win.hidden = true; } $("#acctBtn")?.focus(); }
function setStatus(msg) { const s = $("#acSt"); if (s) s.textContent = msg; }

async function google() {
  const p = new GoogleAuthProvider();
  p.setCustomParameters({ prompt: "select_account" });
  try { await signInWithPopup(auth, p); closeWin(); }
  catch (e) {
    if (e.code === "auth/popup-blocked" || e.code === "auth/operation-not-supported-in-this-environment") { await signInWithRedirect(auth, p); return; }
    if (e.code === "auth/popup-closed-by-user" || e.code === "auth/cancelled-popup-request") return;
    setStatus(msgFor(e));
  }
}
async function sendLink(email) {
  setStatus("Sending…");
  try {
    await sendSignInLinkToEmail(auth, email, { url: location.origin + location.pathname + location.hash, handleCodeInApp: true });
    ls.set(EMAIL_KEY, email);
    setStatus(`Sent. Open the email we sent to ${email} and tap the link. (It may take a minute; check your spam folder too.)`);
  } catch (e) { setStatus(msgFor(e)); }
}
async function finishEmail(email) {
  setStatus("Signing in…");
  try {
    await signInWithEmailLink(auth, email, location.href);
    try { localStorage.removeItem(EMAIL_KEY); } catch (e) {}
    history.replaceState(null, "", location.origin + location.pathname + location.hash);
    closeWin();
  } catch (e) { setStatus(msgFor(e)); }
}
function msgFor(e) {
  const c = (e && e.code) || "";
  if (c.includes("invalid-email")) return "That email address doesn't look right.";
  if (c.includes("expired") || c.includes("invalid-action-code")) return "This sign-in link has expired or was already used. Please ask for a new one.";
  if (c.includes("network")) return "No connection. Please try again when you're online.";
  if (c.includes("unauthorized-domain")) return "Sign-in isn't switched on for this address yet.";
  return "Something went wrong. Please try again.";
}

/* ---------------- start ---------------- */
if (isSignInWithEmailLink(auth, location.href)) {
  const email = ls.get(EMAIL_KEY);
  if (email) finishEmail(email); else openWin("confirm");
}
getRedirectResult(auth).catch(() => {});
onAuthStateChanged(auth, async (u) => {
  const was = user && user.uid;
  user = u;
  document.documentElement.classList.toggle("signed-in", !!u);   // e.g. "progress is saved to your account"
  refreshButton();
  if (u && u.uid !== was) { try { await sync(); } catch (e) { setStatus("Couldn't reach your account just now."); } }
  if (win && !win.hidden) openWin();
});
