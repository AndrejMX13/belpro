'use strict';

// frontend/js/errors.js
// Health widget (shown on volunteers/main page) + App log page (Dnevnik napak)

const SERVICE_LABELS = {
  postgres:  'PostgreSQL',
  whisper:   'Whisper',
  n8n:       'n8n',
  evolution: 'WhatsApp',
  disk:      'Disk',
  heartbeat: 'Heartbeat',
};

// ── Health widget ─────────────────────────────────────────────────────────────

let _healthInterval = null;

function renderHealthWidget(data) {
  const rows = document.getElementById('health-rows');
  if (!rows) return;
  rows.innerHTML = '';

  for (const [key, val] of Object.entries(data)) {
    const label  = SERVICE_LABELS[key] || key;
    const status = val.status || 'ok';
    const dotClass = status === 'ok'      ? 'health-dot-ok'
                   : status === 'warning' ? 'health-dot-warning'
                                          : 'health-dot-error';

    let detail = '';
    if (key === 'postgres' && val.response_ms != null) {
      detail = `${val.response_ms} ms`;
    } else if (key === 'evolution' && val.connection_state) {
      detail = val.connection_state;
    } else if (key === 'disk' && val.free_gb != null) {
      detail = `${val.free_gb} GB free (${val.free_pct}%)`;
    } else if (key === 'heartbeat') {
      const lastEntry = val.last_entry ? new Date(val.last_entry).toLocaleString('sl-SI') : '—';
      detail = `zadnji vnos: ${lastEntry}`;
    } else if (val.detail) {
      detail = val.detail;
    }

    rows.insertAdjacentHTML('beforeend', `
      <div class="health-row">
        <span class="health-dot ${dotClass}"></span>
        <span class="health-label">${label}</span>
        <span class="health-detail">${detail}</span>
      </div>
    `);
  }

  const updated = document.getElementById('health-last-updated');
  if (updated) updated.textContent = `Posodobljeno: ${new Date().toLocaleTimeString('sl-SI')}`;
}

async function loadHealthWidget() {
  try {
    const data = await API.health.detailed();
    renderHealthWidget(data);
  } catch (e) {
    const rows = document.getElementById('health-rows');
    if (rows) rows.innerHTML = '<span style="color:#ef4444">Napaka pri nalaganju stanja.</span>';
  }
}

function startHealthWidget() {
  loadHealthWidget();
  _healthInterval = setInterval(loadHealthWidget, 30_000);
}

function stopHealthWidget() {
  if (_healthInterval) { clearInterval(_healthInterval); _healthInterval = null; }
}

// ── Nav badge (unacknowledged error count) ────────────────────────────────────

async function refreshErrorBadge() {
  try {
    const data  = await API.errors.unacknowledgedCount();
    const badge = document.getElementById('nav-error-badge');
    if (!badge) return;
    if (data.count > 0) {
      badge.textContent = data.count;
      badge.hidden = false;
    } else {
      badge.hidden = true;
    }
  } catch (_) { /* ignore */ }
}

// ── App log page ──────────────────────────────────────────────────────────────

let _applogUnackedOnly = true;

async function loadAppLog() {
  const list = document.getElementById('applog-list');
  if (!list) return;
  list.innerHTML = '<p style="color:#888">Nalaganje...</p>';

  try {
    const errors = await API.errors.list(_applogUnackedOnly);
    if (errors.length === 0) {
      list.innerHTML = '<p style="color:#888">Ni vnosov.</p>';
      return;
    }
    list.innerHTML = errors.map(e => `
      <div class="error-row ${e.acknowledged ? 'acknowledged' : ''}" data-id="${e.id}">
        <div class="error-meta">
          ${esc(e.service)} &middot; ${esc(e.operation)} &middot; ${new Date(e.created_at).toLocaleString('sl-SI')}
          ${e.acknowledged ? '' : `<button class="btn btn-sm" onclick="acknowledgeError('${e.id}')" style="margin-left:0.5rem">Potrdi</button>`}
        </div>
        <div class="error-message">${esc(e.message)}</div>
        ${e.detail ? `<div class="error-detail">${esc(e.detail)}</div>` : ''}
      </div>
    `).join('');
  } catch (err) {
    list.innerHTML = '<p style="color:#ef4444">Napaka pri nalaganju.</p>';
  }
}

window.acknowledgeError = async function(id) {
  try {
    await API.errors.acknowledge(id);
    await loadAppLog();
    await refreshErrorBadge();
  } catch (e) {
    alert('Napaka pri potrditvi.');
  }
};

function initAppLogPage() {
  _applogUnackedOnly = true;
  const filter = document.getElementById('applog-filter-unacked');
  if (filter) {
    filter.checked = true;
    filter.addEventListener('change', () => {
      _applogUnackedOnly = filter.checked;
      loadAppLog();
    });
  }
  loadAppLog();
}

// ── Health widget HTML (injected by renderList in volunteers.js) ──────────────

function healthWidgetHTML() {
  return `
    <div id="health-widget" class="health-widget card" style="margin-bottom:1.5rem">
      <div class="card-header" style="display:flex;align-items:center;gap:0.5rem">
        <span style="font-weight:600">Stanje sistema</span>
        <span id="health-last-updated" style="font-size:0.78rem;color:#888;margin-left:auto"></span>
      </div>
      <div id="health-rows" class="health-rows">
        <span style="color:#888;font-size:0.9rem">Nalaganje...</span>
      </div>
    </div>
  `;
}

// ── App log page HTML (rendered by the router) ────────────────────────────────

function renderAppLog() {
  $('topbar-title').textContent = 'Dnevnik napak';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="applog"]')?.classList.add('active');

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Dnevnik napak</h1>
      <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.9rem">
        <input type="checkbox" id="applog-filter-unacked" checked> Samo nepotrjene
      </label>
    </div>
    <div id="applog-list"></div>
  `);

  initAppLogPage();
}
