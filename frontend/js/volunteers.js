'use strict';

// ===== Validation helpers =====
function _davcnaValid(digits) {
  // Modulus 11 check digit algorithm for Slovenian tax number (davčna številka).
  const weights = [8, 7, 6, 5, 4, 3, 2];
  const total = weights.reduce((sum, w, i) => sum + w * parseInt(digits[i], 10), 0);
  const remainder = total % 11;
  let check = 11 - remainder;
  if (check === 10) check = 0;
  if (check === 11) check = 1;
  return parseInt(digits[7], 10) === check;
}

// ===== DOM helpers =====
function $(id) { return document.getElementById(id); }
function setHtml(el, content) { el.innerHTML = content; }
function show(el) { el.hidden = false; }
function hide(el) { el.hidden = true; }

// ===== Toast =====
function toast(msg, type = 'success') {
  let container = $('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  t.className = 'toast toast-' + type;
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ===== Auth / Login =====
function showLogin() {
  hide($('app'));
  show($('login-screen'));
  $('login-error').hidden = true;
  $('login-password').value = '';
  setTimeout(() => $('login-password').focus(), 50);
}

function showApp() {
  hide($('login-screen'));
  show($('app'));
}

$('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  API.setPassword($('login-password').value);
  try {
    await API.health();
    showApp();
    await checkManagerSetup();
  } catch {
    API.clear();
    $('login-error').hidden = false;
  }
});

$('logout-btn').addEventListener('click', () => {
  API.clear();
  showLogin();
});

window.addEventListener('belpro:unauthorized', showLogin);

// ===== Manager setup check =====
async function checkManagerSetup() {
  try {
    await API.managers.me();
    route();
  } catch (err) {
    if (err.status === 404) {
      openManagerSetupModal();
    } else {
      throw err;
    }
  }
}

function openManagerSetupModal() {
  // Not dismissible — required first-time setup.
  $('modal-title').textContent = 'Prva nastavitev — profil organizacije';
  setHtml($('modal-body'), `
    <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:1.25rem">
      Pred začetkom izpolnite podatke o upravljavcu in organizaciji.
      Ti podatki se bodo pojavili v mesečnih poročilih.
    </p>
    <form id="setup-form" novalidate>
      <p style="font-weight:600;margin-bottom:0.75rem;font-size:0.85rem">Upravljavec</p>
      <div class="form-row">
        <div class="field"><label>Ime *</label><input type="text" name="first_name" required autocomplete="given-name" /></div>
        <div class="field"><label>Priimek *</label><input type="text" name="last_name" required autocomplete="family-name" /></div>
      </div>
      <div class="form-row">
        <div class="field"><label>Telefon *</label><input type="tel" name="phone" required placeholder="+386 1 234 5678" /></div>
        <div class="field"><label>E-pošta *</label><input type="email" name="email" required autocomplete="email" /></div>
      </div>
      <p style="font-weight:600;margin:1rem 0 0.75rem;font-size:0.85rem">Organizacija (NVO)</p>
      <div class="field"><label>Ime organizacije *</label><input type="text" name="ngo_name" required autocomplete="organization" /></div>
      <div class="field"><label>Ulica in hišna številka *</label><input type="text" name="ngo_street" required /></div>
      <div class="form-row">
        <div class="field">
          <label>Poštna številka *</label>
          <input type="text" name="ngo_postal_code" pattern="\\d{4}" maxlength="4" placeholder="1000" required inputmode="numeric" />
        </div>
        <div class="field"><label>Kraj *</label><input type="text" name="ngo_city" required /></div>
      </div>
      <div id="setup-error" class="form-error" hidden></div>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary" id="setup-submit">Shrani in začni</button>
      </div>
    </form>
  `);
  // Show modal without attaching the normal close handlers.
  show($('modal-overlay'));
  $('modal-close').hidden = true;
  $('setup-form').addEventListener('submit', submitManagerSetup);
  $('setup-form').querySelector('[name="first_name"]').focus();
}

async function submitManagerSetup(e) {
  e.preventDefault();
  const form = e.target;
  const errEl = $('setup-error');
  const submitBtn = $('setup-submit');

  if (!form.checkValidity()) {
    form.querySelectorAll(':invalid').forEach(el => (el.style.borderColor = 'var(--danger)'));
    errEl.textContent = 'Preverite označena polja.';
    errEl.hidden = false;
    return;
  }

  const data = Object.fromEntries(new FormData(form));
  errEl.hidden = true;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Shranjevanje…';

  try {
    await API.managers.setup(data);
    hide($('modal-overlay'));
    $('modal-close').hidden = false;
    toast('Nastavitev uspešno shranjena. Dobrodošli!');
    route();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.hidden = false;
    submitBtn.disabled = false;
    submitBtn.textContent = 'Shrani in začni';
  }
}

// ===== Sidebar (mobile) =====
const _sidebar = $('sidebar');

$('hamburger').addEventListener('click', () => _sidebar.classList.toggle('open'));

document.addEventListener('click', (e) => {
  if (_sidebar.classList.contains('open')
      && !_sidebar.contains(e.target)
      && !e.target.closest('#hamburger')) {
    _sidebar.classList.remove('open');
  }
});

document.querySelectorAll('.nav-item[data-page]').forEach(link => {
  link.addEventListener('click', () => _sidebar.classList.remove('open'));
});

// ===== Router =====
function route() {
  const hash = location.hash || '#volunteers';
  if (/^#volunteers\/[^\/]+\/log\/[^\/]+$/.test(hash)) {
    const parts = hash.split('/');
    renderLogEntryDetail(parts[3], {
      backHash: `#volunteers/${parts[1]}`,
      backLabel: '← Nazaj na prostovoljca',
      backNav: 'volunteers',
      goBack: () => renderDetail(parts[1]),
    });
  } else if (/^#approvals\/volunteer\/[^\/]+$/.test(hash)) {
    renderDetail(hash.split('/')[2], {
      backHash:  '#approvals',
      backLabel: '← Nazaj na dnevnike',
      goBack:    renderApprovals,
    });
  } else if (/^#approvals\/[^\/]+\/volunteer\/[^\/]+$/.test(hash)) {
    const parts = hash.split('/');
    const entryId = parts[1];
    const volId   = parts[3];
    renderDetail(volId, {
      backHash:  `#approvals/${entryId}`,
      backLabel: '← Nazaj na vnos',
      goBack:    () => renderLogEntryDetail(entryId),
    });
  } else if (hash.startsWith('#volunteers/')) {
    renderDetail(hash.slice('#volunteers/'.length));
  } else if (hash.startsWith('#approvals/')) {
    renderLogEntryDetail(hash.slice('#approvals/'.length));
  } else if (hash === '#approvals') {
    renderApprovals();
  } else if (/^#reports\/volunteer\/[^\/]+$/.test(hash)) {
    renderDetail(hash.split('/')[2], {
      backHash:  '#reports',
      backLabel: '← Nazaj na poročila',
      goBack:    renderReports,
    });
  } else if (hash === '#reports') {
    renderReports();
  } else if (hash === '#analytics') {
    renderAnalytics();
  } else if (hash === '#settings') {
    renderSettings();
  } else {
    renderList();
  }
}

window.addEventListener('hashchange', route);

// ===== State =====
const state = {
  filter: {
    active: true,
    search_by: 'last_name',
    search_q: '',
    sort_by: 'last_name',
    sort_dir: 'asc',
    offset: 0,
    limit: 20,
  },
  total: 0,
  items: [],
};

// Blob URLs created for photo thumbnails — revoked on navigation to prevent memory leaks.
const _photoObjectUrls = [];
function revokePhotoUrls() {
  _photoObjectUrls.forEach(u => URL.revokeObjectURL(u));
  _photoObjectUrls.length = 0;
}

const approvalsState = {
  filter: { status: 'pending_manager', search_q: '', date_from: null, date_to: null, date_field: 'work_date', sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 },
  total: 0,
  items: [],
  volunteerMap: new Map(),
};

const volunteerLogState = {
  volunteerId: null,
  filter: { status: '', search_q: '', date_from: null, date_to: null, date_field: 'work_date', sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 },
  total: 0,
  items: [],
};


// ===== Lookup tables =====
const STATUS_LABEL = {
  pending_volunteer: 'Čaka prostovoljca',
  pending_manager:   'Čaka odobritev',
  approved:          'Odobreno',
  rejected:          'Zavrnjeno',
};

const STATUS_BADGE_CLASS = {
  pending_volunteer: 'badge-pending',
  pending_manager:   'badge-pending',
  approved:          'badge-approved',
  rejected:          'badge-rejected',
};

function statusBadge(s) {
  return `<span class="badge ${STATUS_BADGE_CLASS[s] || ''}">${esc(STATUS_LABEL[s] || s)}</span>`;
}

// ===== Volunteers list =====
async function renderList() {
  $('topbar-title').textContent = 'Prostovoljci';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="volunteers"]')?.classList.add('active');

  const activeOpt   = (v) => state.filter.active    === v ? ' selected' : '';
  const searchByOpt = (v) => state.filter.search_by === v ? ' selected' : '';

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Prostovoljci</h1>
      <button class="btn btn-primary" id="add-btn">+ Dodaj prostovoljca</button>
    </div>
    <div class="filter-bar">
      <select id="f-active">
        <option value=""${activeOpt('')}>Vsi</option>
        <option value="true"${activeOpt(true)}>Aktivni</option>
        <option value="false"${activeOpt(false)}>Neaktivni</option>
      </select>
      <select id="f-search-by">
        <option value="last_name"${searchByOpt('last_name')}>Priimek</option>
        <option value="first_name"${searchByOpt('first_name')}>Ime</option>
        <option value="name"${searchByOpt('name')}>Ime ali priimek</option>
        <option value="city"${searchByOpt('city')}>Mesto</option>
        <option value="phone"${searchByOpt('phone')}>Telefon</option>
      </select>
      <input type="text" id="f-search-q" placeholder="Iskanje…"
             value="${esc(state.filter.search_q)}" style="flex:1;min-width:130px;max-width:220px" />
      <button class="btn btn-primary btn-sm" id="f-search">Išči</button>
      <button class="btn btn-ghost btn-sm" id="f-reset">Ponastavi</button>
    </div>
    <div class="table-wrapper">
      <table id="volunteers-table">
        <thead><tr id="volunteers-head">
          ${renderThead()}
        </tr></thead>
        <tbody id="volunteers-body">
          <tr class="loading-row"><td colspan="6"><span class="spinner"></span></td></tr>
        </tbody>
      </table>
    </div>
    <div class="pagination">
      <span id="pg-info"></span>
      <div class="pagination-btns">
        <button id="prev-btn">← Nazaj</button>
        <button id="next-btn">Naprej →</button>
      </div>
    </div>
  `);

  $('add-btn').addEventListener('click', openAddModal);
  $('f-active').addEventListener('change', applyFilters);
  $('f-search').addEventListener('click', applyFilters);
  $('f-reset').addEventListener('click', resetFilters);
  $('f-search-q').addEventListener('keydown', e => { if (e.key === 'Enter') applyFilters(); });
  $('prev-btn').addEventListener('click', () => {
    state.filter.offset = Math.max(0, state.filter.offset - state.filter.limit);
    loadVolunteers();
  });
  $('next-btn').addEventListener('click', () => {
    state.filter.offset += state.filter.limit;
    loadVolunteers();
  });

  $('volunteers-table').addEventListener('click', (e) => {
    const th = e.target.closest('th[data-sort]');
    if (!th) return;
    const col = th.dataset.sort;
    if (state.filter.sort_by === col) {
      state.filter.sort_dir = state.filter.sort_dir === 'asc' ? 'desc' : 'asc';
    } else {
      state.filter.sort_by = col;
      state.filter.sort_dir = 'asc';
    }
    state.filter.offset = 0;
    loadVolunteers();
  });

  await loadVolunteers();
}

function renderThead() {
  return `
    ${sortTh('Ime in priimek', 'last_name')}
    ${sortTh('Telefon', 'phone')}
    ${sortTh('Mesto', 'city')}
    <th>Ure ta mesec</th>
    ${sortTh('Status', 'active')}
    <th>Akcije</th>
  `;
}

function sortTh(label, col) {
  const active = state.filter.sort_by === col ? ' sort-active' : '';
  const arrow = state.filter.sort_by === col
    ? (state.filter.sort_dir === 'asc' ? '↑' : '↓')
    : '↕';
  return `<th class="sortable${active}" data-sort="${col}">${esc(label)} <span class="sort-arrow">${arrow}</span></th>`;
}

async function loadVolunteers() {
  const tbody = $('volunteers-body');
  if (!tbody) return;

  const params = {};
  if (state.filter.active !== '') params.active = state.filter.active;
  if (state.filter.search_q) {
    params.search_by = state.filter.search_by;
    params.search_q  = state.filter.search_q;
  }
  params.sort_by  = state.filter.sort_by;
  params.sort_dir = state.filter.sort_dir;
  params.offset   = state.filter.offset;
  params.limit    = state.filter.limit;

  try {
    const data = await API.volunteers.list(params);
    state.total = data.total;
    state.items = data.items;
    const head = $('volunteers-head');
    if (head) setHtml(head, renderThead());
    renderTable(data.items);
    renderPagination();
  } catch (err) {
    setHtml(tbody, `<tr class="empty-row"><td colspan="6">Napaka: ${esc(err.message)}</td></tr>`);
  }
}

function renderTable(items) {
  const tbody = $('volunteers-body');
  if (!tbody) return;

  if (!items.length) {
    setHtml(tbody, `<tr class="empty-row"><td colspan="6">Ni prostovoljcev, ki ustrezajo filtrom.</td></tr>`);
    return;
  }

  tbody.innerHTML = items.map(v => `
    <tr data-id="${v.id}">
      <td><strong>${esc(v.first_name + ' ' + v.last_name)}</strong></td>
      <td>${esc(v.phone)}</td>
      <td>${esc(v.city)}</td>
      <td>${v.hours_this_month != null ? fmtHours(v.hours_this_month) : '—'}</td>
      <td>${v.active
            ? '<span class="badge badge-active">Aktiven</span>'
            : '<span class="badge badge-inactive">Neaktiven</span>'}</td>
      <td class="td-actions" data-stop>
        ${v.active
          ? `<button class="btn btn-danger btn-sm deactivate-btn"
                data-id="${v.id}" data-name="${esc(v.first_name + ' ' + v.last_name)}">Deaktiviraj</button>`
          : `<button class="btn btn-secondary btn-sm activate-btn"
                data-id="${v.id}" data-name="${esc(v.first_name + ' ' + v.last_name)}">Aktiviraj</button>`}
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr[data-id]').forEach(row => {
    row.addEventListener('click', (e) => {
      if (e.target.closest('[data-stop]')) return;
      location.hash = '#volunteers/' + row.dataset.id;
    });
  });

  tbody.querySelectorAll('.deactivate-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const { id, name } = btn.dataset;
      if (!confirm(`Deaktiviraj prostovoljca ${name}?\n\nTa oseba ne bo več mogla beležiti dela.`)) return;
      btn.disabled = true;
      btn.textContent = '…';
      try {
        await API.volunteers.deactivate(id);
        toast(`${name} je bil deaktiviran.`);
        await loadVolunteers();
      } catch (err) {
        toast('Napaka: ' + err.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Deaktiviraj';
      }
    });
  });

  tbody.querySelectorAll('.activate-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const { id, name } = btn.dataset;
      if (!confirm(`Aktiviraj prostovoljca ${name}?\n\nTa oseba bo spet lahko beležila delo.`)) return;
      btn.disabled = true;
      btn.textContent = '…';
      try {
        await API.volunteers.activate(id);
        toast(`${name} je bil aktiviran.`);
        await loadVolunteers();
      } catch (err) {
        toast('Napaka: ' + err.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Aktiviraj';
      }
    });
  });
}

function renderPagination() {
  const from   = state.total === 0 ? 0 : state.filter.offset + 1;
  const to     = Math.min(state.filter.offset + state.filter.limit, state.total);
  const info   = $('pg-info');
  const prevBtn = $('prev-btn');
  const nextBtn = $('next-btn');
  if (info)    info.textContent = state.total > 0 ? `Prikazujem ${from}–${to} od ${state.total}` : 'Ni rezultatov';
  if (prevBtn) prevBtn.disabled = state.filter.offset === 0;
  if (nextBtn) nextBtn.disabled = state.filter.offset + state.filter.limit >= state.total;
}

function applyFilters() {
  const v = $('f-active')?.value;
  state.filter.active    = v === 'true' ? true : v === 'false' ? false : '';
  state.filter.search_by = $('f-search-by')?.value || 'last_name';
  state.filter.search_q  = $('f-search-q')?.value.trim() || '';
  state.filter.offset    = 0;
  loadVolunteers();
}

function resetFilters() {
  state.filter.active    = true;
  state.filter.search_by = 'last_name';
  state.filter.search_q  = '';
  state.filter.offset    = 0;
  state.filter.sort_by = 'last_name';
  state.filter.sort_dir = 'asc';
  renderList();
}

// ===== Add volunteer modal =====
function wireReportPrefs(masterEl, emailEl, waEl, errEl, onSave) {
  const saveBtn = errEl.parentElement.querySelector('button');

  masterEl.addEventListener('change', () => {
    if (masterEl.checked) {
      emailEl.checked = true;
      waEl.checked = false;
    } else {
      emailEl.checked = false;
      waEl.checked = false;
    }
  });

  function syncMaster() { masterEl.checked = emailEl.checked || waEl.checked; }
  emailEl.addEventListener('change', syncMaster);
  waEl.addEventListener('change', syncMaster);

  if (saveBtn) {
    saveBtn.addEventListener('click', async () => {
      errEl.style.display = 'none';
      saveBtn.disabled = true;
      try {
        await onSave(waEl.checked, emailEl.checked);
      } catch (err) {
        errEl.textContent = err.message;
        errEl.style.display = '';
      } finally {
        saveBtn.disabled = false;
      }
    });
  }
}

async function openAddModal() {
  let defWa = false;
  let defEmail = true;
  try {
    const mgr = await API.managers.me();
    defWa    = mgr.default_report_whatsapp;
    defEmail = mgr.default_report_email;
  } catch { /* use hardcoded defaults if fetch fails */ }

  openModal('Dodaj prostovoljca', `
    <form id="add-form" novalidate>
      <div class="form-row">
        <div class="field"><label>Ime *</label><input type="text" name="first_name" required autocomplete="off" /></div>
        <div class="field"><label>Priimek *</label><input type="text" name="last_name" required autocomplete="off" /></div>
      </div>
      <div class="field"><label>Ulica in hišna številka *</label><input type="text" name="street" required autocomplete="off" /></div>
      <div class="form-row">
        <div class="field">
          <label>Poštna številka *</label>
          <input type="text" name="postal_code" pattern="\\d{4}" maxlength="4" placeholder="1000" required />
          <p class="form-hint">4-mestna številka</p>
        </div>
        <div class="field"><label>Kraj *</label><input type="text" name="city" required autocomplete="off" /></div>
      </div>
      <div class="field">
        <label>EMŠO *</label>
        <input type="text" name="emso" pattern="\\d{13}" minlength="13" maxlength="13" placeholder="0000000000000" required inputmode="numeric" />
        <p class="form-hint">13-mestna številka</p>
      </div>
      <div class="form-row">
        <div class="field"><label>Telefon *</label><input type="tel" name="phone" required placeholder="+386 41 123 456" /></div>
        <div class="field"><label>E-pošta</label><input type="email" name="email" /></div>
      </div>
      <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border)">
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="add-rp-master" ${(defEmail || defWa) ? 'checked' : ''}>
          <span>Pošiljanje mesečnih poročil</span>
        </label>
        <div id="add-rp-sub" style="margin-left:1.5rem;margin-top:0.5rem;display:flex;flex-direction:column;gap:0.4rem">
          <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
            <input type="checkbox" id="add-rp-email" ${defEmail ? 'checked' : ''}> E-pošta
          </label>
          <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
            <input type="checkbox" id="add-rp-whatsapp" ${defWa ? 'checked' : ''}> WhatsApp
          </label>
        </div>
        <div id="add-rp-error" class="form-error" style="display:none"></div>
      </div>
      <div id="add-error" class="form-error" hidden></div>
      <div class="form-actions">
        <button type="button" class="btn btn-ghost" id="cancel-add">Prekliči</button>
        <button type="submit" class="btn btn-primary" id="add-submit">Shrani</button>
      </div>
    </form>
  `);

  // Wire master/sub checkbox logic (no save button — values read on form submit)
  const masterEl = $('add-rp-master');
  const emailEl  = $('add-rp-email');
  const waEl     = $('add-rp-whatsapp');

  masterEl.addEventListener('change', () => {
    if (masterEl.checked) { emailEl.checked = true; waEl.checked = false; }
    else { emailEl.checked = false; waEl.checked = false; }
  });
  function syncAddMaster() { masterEl.checked = emailEl.checked || waEl.checked; }
  emailEl.addEventListener('change', syncAddMaster);
  waEl.addEventListener('change', syncAddMaster);

  $('cancel-add').addEventListener('click', closeModal);
  $('add-form').addEventListener('submit', submitAddVolunteer);
  $('add-form').querySelector('[name="first_name"]').focus();
}

async function submitAddVolunteer(e) {
  e.preventDefault();
  const form    = e.target;
  const errEl   = $('add-error');
  const submitBtn = $('add-submit');

  // Basic HTML5 validation
  if (!form.checkValidity()) {
    form.querySelectorAll(':invalid').forEach(el => el.style.borderColor = 'var(--danger)');
    errEl.textContent = 'Preverite označena polja.';
    errEl.hidden = false;
    return;
  }

  const data = Object.fromEntries(new FormData(form));
  if (!data.email) delete data.email;
  // FormData omits unchecked checkboxes — read them explicitly
  data.report_email    = $('add-rp-email')?.checked ?? true;
  data.report_whatsapp = $('add-rp-whatsapp')?.checked ?? false;

  // 1. Hard block — EMŠO duplicate (check server-side before anything else)
  errEl.hidden = true;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Preverjanje…';
  try {
    const { exists } = await API.volunteers.checkEmso(data.emso);
    if (exists) {
      errEl.textContent = 'Prostovoljec s tem EMŠO-jem že obstaja.';
      errEl.hidden = false;
      submitBtn.disabled = false;
      submitBtn.textContent = 'Shrani';
      return;
    }
  } catch (err) {
    errEl.textContent = 'Napaka pri preverjanju EMŠO: ' + err.message;
    errEl.hidden = false;
    submitBtn.disabled = false;
    submitBtn.textContent = 'Shrani';
    return;
  }

  // 2. Soft warning — duplicate name (confirmation required)
  const fullName = (data.first_name + ' ' + data.last_name).trim().toLowerCase();
  const nameDupe = state.items.find(v =>
    (v.first_name + ' ' + v.last_name).toLowerCase() === fullName
  );
  if (nameDupe) {
    const proceed = confirm(
      `Prostovoljec s tem imenom (${data.first_name} ${data.last_name}) že obstaja.\n\n` +
      `Ali ste prepričani, da gre za drugo osebo?`
    );
    if (!proceed) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Shrani';
      return;
    }
  }

  // 3. Submit — phone duplicate surfaces here as a 409 if it slips through
  submitBtn.textContent = 'Shranjevanje…';
  try {
    await API.volunteers.create(data);
    closeModal();
    toast('Prostovoljec uspešno dodan.');
    state.filter.offset = 0;
    await loadVolunteers();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.hidden = false;
    submitBtn.disabled = false;
    submitBtn.textContent = 'Shrani';
  }
}

// ===== Volunteer detail =====
async function renderDetail(id, { backHash = '#volunteers', backLabel = '← Nazaj na seznam', goBack = null } = {}) {
  $('topbar-title').textContent = 'Prostovoljec';
  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  if (volunteerLogState.volunteerId !== id) {
    volunteerLogState.volunteerId = id;
    volunteerLogState.filter = { status: '', search_q: '', date_from: null, date_to: null, date_field: 'work_date', sort_by: 'work_date', sort_dir: 'desc', offset: 0, limit: 20 };
    volunteerLogState.total = 0;
    volunteerLogState.items = [];
  }

  try {
    const v = await API.volunteers.get(id);
    const initials = (v.first_name[0] + v.last_name[0]).toUpperCase();

    const statusOpt = (val, label) => {
      const sel = volunteerLogState.filter.status === val ? ' selected' : '';
      return `<option value="${val}"${sel}>${label}</option>`;
    };

    setHtml($('main-content'), `
      <button class="back-link" id="back-btn">${backLabel}</button>

      <div class="detail-header">
        <div class="detail-avatar" id="vol-avatar">${initials}</div>
        <div>
          <div class="detail-name" style="display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap">
            <span id="vol-name-text">${esc(v.first_name + ' ' + v.last_name)}</span>
            <button class="btn btn-ghost btn-sm" id="vol-name-pencil" title="Uredi ime" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-name-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-fname" value="${esc(v.first_name)}" maxlength="100" style="width:7rem">
              <input type="text" id="vol-lname" value="${esc(v.last_name)}" maxlength="100" style="width:9rem">
              <button class="btn btn-primary btn-sm" id="vol-name-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-name-cancel">Prekliči</button>
              <span id="vol-name-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
          </div>
          <div class="detail-meta" style="display:flex;align-items:center;gap:0.3rem;flex-wrap:wrap;margin-top:0.2rem">
            <span id="vol-phone-text">${esc(v.phone)}</span>
            <button class="btn btn-ghost btn-sm" id="vol-phone-pencil" title="Uredi telefon" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-phone-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-phone-inp" value="${esc(v.phone)}" maxlength="30" style="width:12rem">
              <button class="btn btn-primary btn-sm" id="vol-phone-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-phone-cancel">Prekliči</button>
              <span id="vol-phone-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
            <span id="vol-email-sep">${v.email ? ' · ' : ''}</span>
            <span id="vol-email-text">${v.email ? esc(v.email) : ''}</span>
            <button class="btn btn-ghost btn-sm" id="vol-email-pencil" title="Uredi e-pošto" style="padding:0.1rem 0.4rem;font-size:0.85rem">✏</button>
            <span id="vol-email-inputs" style="display:none;align-items:center;gap:0.3rem;flex-wrap:wrap">
              <input type="text" id="vol-email-inp" value="${v.email ? esc(v.email) : ''}" maxlength="255" style="width:14rem" placeholder="E-poštni naslov (neobvezno)">
              <button class="btn btn-primary btn-sm" id="vol-email-save">Shrani</button>
              <button class="btn btn-ghost btn-sm" id="vol-email-cancel">Prekliči</button>
              <span id="vol-email-err" class="form-error" style="width:100%;font-size:0.75rem"></span>
            </span>
          </div>
          <div style="margin-top:0.4rem">
            ${v.active
              ? '<span class="badge badge-active">Aktiven</span>'
              : '<span class="badge badge-inactive">Neaktiven</span>'}
          </div>
        </div>
      </div>

      <div class="detail-info-grid">
        <div class="info-item">
          <div class="info-label">Naslov</div>
          <div class="info-value">${esc(v.street)}, ${esc(v.postal_code)} ${esc(v.city)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">EMŠO</div>
          <div class="info-value">${esc(v.emso_masked)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Ure ta mesec</div>
          <div class="info-value">${fmtHours(v.hours_this_month)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Registriran</div>
          <div class="info-value">${fmtDatetime(v.registered_at)}</div>
        </div>
      </div>

      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin-bottom:1.5rem">
        <p class="section-title" style="margin-top:0">Mesečna poročila</p>
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="rp-master" ${(v.report_email || v.report_whatsapp) ? 'checked' : ''}>
          <span>Pošiljanje mesečnih poročil</span>
        </label>
        <div id="rp-sub" style="margin-left:1.5rem;margin-top:0.5rem;display:flex;flex-direction:column;gap:0.4rem">
          <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
            <input type="checkbox" id="rp-email" ${v.report_email ? 'checked' : ''}> E-pošta
          </label>
          <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
            <input type="checkbox" id="rp-whatsapp" ${v.report_whatsapp ? 'checked' : ''}> WhatsApp
          </label>
        </div>
        <div id="rp-error" class="form-error" style="display:none"></div>
        <div class="form-actions" style="margin-top:0.75rem">
          <button class="btn btn-primary btn-sm" id="rp-save">Shrani</button>
        </div>
      </div>

      ${v.log_entries.length === 0 ? `
        <div style="margin:0 0 1.5rem">
          <button class="btn btn-danger btn-sm" id="delete-btn">Izbriši prostovoljca</button>
          <span style="font-size:0.8rem;color:var(--text-muted);margin-left:0.75rem">Samo prostovoljci brez vnosov se lahko izbrišejo.</span>
        </div>
      ` : ''}

      <p class="section-title">Dnevnik dela</p>
      <div style="margin-bottom:1rem">
        <button class="btn btn-primary btn-sm" id="add-entry-btn">+ Dodaj vnos</button>
      </div>

      <div class="filter-bar">
        <select id="vlog-status">
          ${statusOpt('', 'Vsi statusi')}
          ${statusOpt('pending_volunteer', 'Čaka prostovoljca')}
          ${statusOpt('pending_manager', 'Čaka odobritev')}
          ${statusOpt('approved', 'Odobreno')}
          ${statusOpt('rejected', 'Zavrnjeno')}
        </select>
        <label style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center;display:flex;align-items:center;gap:0.3rem;cursor:pointer">
          <input type="checkbox" id="vlog-date-field-cb" ${volunteerLogState.filter.date_field === 'created_at' ? 'checked' : ''} />
          Dan vnosa
        </label>
        <label for="vlog-date-from" style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center">Od:</label>
        <input type="date" id="vlog-date-from" value="${volunteerLogState.filter.date_from || ''}" />
        <label for="vlog-date-to" style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center">Do:</label>
        <input type="date" id="vlog-date-to" value="${volunteerLogState.filter.date_to || ''}" />
        <input type="text" id="vlog-search-q" placeholder="Iskanje po opisu ali lokaciji…"
               value="${esc(volunteerLogState.filter.search_q)}" style="flex:1;min-width:130px;max-width:280px" />
        <button class="btn btn-primary btn-sm" id="vlog-search">Išči</button>
        <button class="btn btn-ghost btn-sm" id="vlog-reset">Ponastavi</button>
      </div>

      <div class="table-wrapper">
        <table id="vlog-table">
          <thead><tr id="vlog-head">${renderVolunteerLogThead()}</tr></thead>
          <tbody id="vlog-body"><tr class="loading-row"><td colspan="6">Nalaganje…</td></tr></tbody>
        </table>
      </div>

      <div class="pagination">
        <span id="vlog-pg-info"></span>
        <div class="pagination-btns">
          <button id="vlog-prev-btn" disabled>← Prejšnja</button>
          <button id="vlog-next-btn" disabled>Naslednja →</button>
        </div>
      </div>
    `);

    $('back-btn').addEventListener('click', () => {
      history.pushState(null, '', backHash);
      (goBack || renderList)();
    });

    function wireInlineEdit({ pencilId, inputsId, textId, saveId, cancelId, errId, validate, getPayload, onSuccess }) {
      const pencilEl = $(pencilId);
      const inputsEl = $(inputsId);
      const textEl   = $(textId);
      const saveEl   = $(saveId);
      const cancelEl = $(cancelId);
      const errEl    = $(errId);

      const inputs = Array.from(inputsEl.querySelectorAll('input'));
      let savedValues = [];

      function enterEdit() {
        savedValues            = inputs.map(inp => inp.value);
        textEl.hidden          = true;
        pencilEl.hidden        = true;
        inputsEl.style.display = 'flex';
        errEl.textContent      = '';
        inputs[0].focus();
      }

      function exitEdit() {
        inputsEl.style.display = 'none';
        textEl.hidden          = false;
        pencilEl.hidden        = false;
        errEl.textContent      = '';
      }

      pencilEl.addEventListener('click', enterEdit);

      // Restore values typed but not saved so the zone reopens clean.
      cancelEl.addEventListener('click', () => {
        inputs.forEach((inp, i) => { inp.value = savedValues[i]; });
        exitEdit();
      });

      saveEl.addEventListener('click', async () => {
        const validationErr = validate ? validate() : null;
        if (validationErr) { errEl.textContent = validationErr; return; }
        saveEl.disabled    = true;
        saveEl.textContent = 'Shranjevanje…';
        try {
          await API.volunteers.update(id, getPayload());
          onSuccess();
          exitEdit();
          toast('Podatki so bili shranjeni.');
        } catch (e) {
          errEl.textContent = e?.message || String(e) || 'Napaka pri shranjevanju.';
        } finally {
          saveEl.disabled    = false;
          saveEl.textContent = 'Shrani';
        }
      });
    }

    // Name zone
    wireInlineEdit({
      pencilId: 'vol-name-pencil', inputsId: 'vol-name-inputs',
      textId:   'vol-name-text',   saveId:   'vol-name-save',
      cancelId: 'vol-name-cancel', errId:    'vol-name-err',
      validate: () => {
        if (!$('vol-fname').value.trim()) return 'Ime ne sme biti prazno.';
        if (!$('vol-lname').value.trim()) return 'Priimek ne sme biti prazen.';
        return null;
      },
      getPayload: () => ({
        first_name: $('vol-fname').value.trim(),
        last_name:  $('vol-lname').value.trim(),
      }),
      onSuccess: () => {
        const fn = $('vol-fname').value.trim();
        const ln = $('vol-lname').value.trim();
        $('vol-name-text').textContent = fn + ' ' + ln;
        $('vol-avatar').textContent    = (fn[0] + ln[0]).toUpperCase();
      },
    });

    // Phone zone
    wireInlineEdit({
      pencilId: 'vol-phone-pencil', inputsId: 'vol-phone-inputs',
      textId:   'vol-phone-text',   saveId:   'vol-phone-save',
      cancelId: 'vol-phone-cancel', errId:    'vol-phone-err',
      validate: () => {
        if (!$('vol-phone-inp').value.trim()) return 'Telefonska številka ne sme biti prazna.';
        return null;
      },
      getPayload: () => ({ phone: $('vol-phone-inp').value.trim() }),
      onSuccess: () => {
        $('vol-phone-text').textContent = $('vol-phone-inp').value.trim();
      },
    });

    // Email zone
    wireInlineEdit({
      pencilId: 'vol-email-pencil', inputsId: 'vol-email-inputs',
      textId:   'vol-email-text',   saveId:   'vol-email-save',
      cancelId: 'vol-email-cancel', errId:    'vol-email-err',
      validate: null,
      getPayload: () => ({ email: $('vol-email-inp').value.trim() }),
      onSuccess: () => {
        const val = $('vol-email-inp').value.trim();
        $('vol-email-text').textContent = val;
        $('vol-email-sep').textContent  = val ? ' · ' : '';
      },
    });

    $('add-entry-btn').addEventListener('click', () => {
      const today = new Date().toISOString().slice(0, 10);
      openModal('Nov vnos', `
        <form id="add-entry-form" novalidate>
          <div class="field" style="max-width:200px">
            <label>Datum dela *</label>
            <input type="date" id="ae-work-date" value="${today}" required />
          </div>
          <div class="field" style="max-width:160px">
            <label>Ure *</label>
            <input type="number" id="ae-hours" min="0.5" max="24" step="0.5" placeholder="npr. 4" required />
          </div>
          <div class="field">
            <label>Opis dela *</label>
            <textarea id="ae-desc" rows="4" style="width:100%;resize:vertical" required></textarea>
          </div>
          <div class="field">
            <label>Lokacija</label>
            <input type="text" id="ae-location" placeholder="Npr. Dom starejših Trnovo" />
          </div>
          <div id="ae-error" class="form-error" hidden></div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" id="ae-submit">Shrani vnos</button>
          </div>
        </form>
      `);

      $('add-entry-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const workDate = $('ae-work-date').value;
        const hours    = parseFloat($('ae-hours').value);
        const desc     = $('ae-desc').value.trim();
        const location = $('ae-location').value.trim() || null;
        const errEl    = $('ae-error');

        if (!workDate) {
          errEl.textContent = 'Datum dela je obvezen.';
          errEl.hidden = false;
          return;
        }
        if (isNaN(hours) || hours < 0.5 || hours > 24) {
          errEl.textContent = 'Ure morajo biti med 0.5 in 24.';
          errEl.hidden = false;
          return;
        }
        if (!desc) {
          errEl.textContent = 'Opis dela ne sme biti prazen.';
          errEl.hidden = false;
          return;
        }

        errEl.hidden = true;
        $('ae-submit').disabled = true;
        $('ae-submit').textContent = 'Shranjevanje…';

        try {
          const entry = await API.logEntries.create({
            volunteer_id: id,
            work_date:    workDate,
            hours,
            activity_description: desc,
            location,
          });
          closeModal();
          toast('Vnos ustvarjen.');
          history.pushState(null, '', `#volunteers/${id}`);
          renderDetail(id);
        } catch (err) {
          errEl.textContent = err.message;
          errEl.hidden = false;
          $('ae-submit').disabled = false;
          $('ae-submit').textContent = 'Shrani vnos';
        }
      });
    });

    const deleteBtn = $('delete-btn');
    if (deleteBtn) {
      deleteBtn.addEventListener('click', async () => {
        const name = v.first_name + ' ' + v.last_name;
        if (!confirm(`Trajno izbriši prostovoljca ${name}?\n\nTega dejanja ni mogoče razveljaviti.`)) return;
        deleteBtn.disabled = true;
        deleteBtn.textContent = 'Brisanje…';
        try {
          await API.volunteers.delete(v.id);
          toast(`${name} je bil izbrisan.`);
          history.pushState(null, '', '#volunteers');
          renderList();
        } catch (err) {
          toast('Napaka: ' + err.message, 'error');
          deleteBtn.disabled = false;
          deleteBtn.textContent = 'Izbriši prostovoljca';
        }
      });
    }

    // Report preferences card
    wireReportPrefs(
      $('rp-master'), $('rp-email'), $('rp-whatsapp'),
      $('rp-error'),
      async (wa, email) => {
        await API.volunteers.update(id, { report_whatsapp: wa, report_email: email });
        toast('Nastavitve poročil so bile shranjene.');
      }
    );

    $('vlog-status').addEventListener('change', () => {
      volunteerLogState.filter.status = $('vlog-status').value;
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    });

    function applyVolLogSearch() {
      volunteerLogState.filter.search_q = $('vlog-search-q')?.value.trim() || '';
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    }

    $('vlog-search').addEventListener('click', applyVolLogSearch);
    $('vlog-search-q').addEventListener('keydown', e => { if (e.key === 'Enter') applyVolLogSearch(); });

    $('vlog-date-field-cb').addEventListener('change', () => {
      volunteerLogState.filter.date_field = $('vlog-date-field-cb').checked ? 'created_at' : 'work_date';
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    });
    $('vlog-date-from').addEventListener('change', () => {
      volunteerLogState.filter.date_from = $('vlog-date-from').value || null;
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    });
    $('vlog-date-to').addEventListener('change', () => {
      volunteerLogState.filter.date_to = $('vlog-date-to').value || null;
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    });

    $('vlog-reset').addEventListener('click', () => {
      volunteerLogState.filter.search_q  = '';
      volunteerLogState.filter.date_from = null;
      volunteerLogState.filter.date_to   = null;
      volunteerLogState.filter.date_field = 'work_date';
      volunteerLogState.filter.status    = '';
      $('vlog-search-q').value        = '';
      $('vlog-date-from').value       = '';
      $('vlog-date-to').value         = '';
      $('vlog-status').value          = '';
      $('vlog-date-field-cb').checked = false;
      volunteerLogState.filter.offset = 0;
      loadVolunteerLog();
    });

    $('vlog-prev-btn').addEventListener('click', () => {
      volunteerLogState.filter.offset = Math.max(0, volunteerLogState.filter.offset - volunteerLogState.filter.limit);
      loadVolunteerLog();
    });

    $('vlog-next-btn').addEventListener('click', () => {
      volunteerLogState.filter.offset += volunteerLogState.filter.limit;
      loadVolunteerLog();
    });

    $('vlog-table').addEventListener('click', async (e) => {
      const th = e.target.closest('th[data-sort]');
      if (th) {
        const col = th.dataset.sort;
        if (volunteerLogState.filter.sort_by === col) {
          volunteerLogState.filter.sort_dir = volunteerLogState.filter.sort_dir === 'asc' ? 'desc' : 'asc';
        } else {
          volunteerLogState.filter.sort_by  = col;
          volunteerLogState.filter.sort_dir = 'asc';
        }
        volunteerLogState.filter.offset = 0;
        await loadVolunteerLog();
        return;
      }

      const row = e.target.closest('tr[data-id]');
      if (row) {
        location.hash = `#volunteers/${id}/log/${row.dataset.id}`;
      }
    });

    await loadVolunteerLog();

  } catch (err) {
    setHtml($('main-content'), `<p style="color:var(--danger);padding:1rem">Napaka: ${esc(err.message)}</p>`);
  }
}

// ===== Modal helpers =====
function openModal(title, bodyHtml) {
  $('modal-title').textContent = title;
  setHtml($('modal-body'), bodyHtml);
  show($('modal-overlay'));
}

function closeModal() {
  hide($('modal-overlay'));
  setHtml($('modal-body'), '');
}

$('modal-close').addEventListener('click', closeModal);
$('modal-overlay').addEventListener('click', (e) => {
  if (e.target === $('modal-overlay')) closeModal();
});

// ===== Utilities =====
function esc(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function fmtDateShort(isoDate) {
  if (!isoDate) return '';
  return new Date(isoDate + 'T00:00:00').toLocaleDateString('sl-SI', { day: 'numeric', month: 'short', year: 'numeric' });
}

function fmtHours(h) {
  return Number(h).toFixed(1) + ' h';
}

function fmtDatetime(iso) {
  if (!iso) return '—';
  return iso.slice(0, 10);
}

// ===== Settings page =====
function _waBadge(state) {
  const map = {
    open:            '<span style="color:var(--success,#16a34a);font-size:0.85rem">✓ Povezano</span>',
    connecting:      '<span style="color:#d97706;font-size:0.85rem">⟳ Vzpostavljanje...</span>',
    close:           '<span style="color:var(--text-muted,#6b7280);font-size:0.85rem">Ni povezano</span>',
    unreachable:     '<span style="color:#dc2626;font-size:0.85rem">⚠ Evolution API nedosegljiv</span>',
    lid_unsupported: '<span style="color:#d97706;font-size:0.85rem">⚠ @lid JID — nadgradite Evolution API</span>',
  };
  return map[state] || '';
}

async function renderSettings() {
  $('topbar-title').textContent = 'Nastavitve';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="settings"]')?.classList.add('active');

  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  let manager, configInfo;
  try {
    [manager, configInfo] = await Promise.all([API.managers.me(), API.managers.configInfo()]);
  } catch (err) {
    setHtml($('main-content'), `<p class="form-error" style="margin:2rem">Napaka: ${esc(err.message)}</p>`);
    return;
  }

  if (configInfo.wa_synced) {
    toast('Številka WhatsApp bota je bila samodejno posodobljena.');
  }

  const card = 'background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-bottom:1.5rem';
  const h2   = 'font-size:1rem;font-weight:600;margin:0 0 1.25rem';

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Nastavitve</h1>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Podatki upravljalca</h2>
      <div class="form-row">
        <div class="field"><label>Ime</label>
          <input id="s-first-name" type="text" value="${esc(manager.first_name)}" required maxlength="100"></div>
        <div class="field"><label>Priimek</label>
          <input id="s-last-name" type="text" value="${esc(manager.last_name)}" required maxlength="100"></div>
      </div>
      <div class="form-row">
        <div class="field"><label>E-pošta</label>
          <input id="s-email" type="email" value="${esc(manager.email)}" required maxlength="255"></div>
        <div class="field"><label>Telefon</label>
          <input id="s-phone" type="tel" value="${esc(manager.phone)}" required maxlength="30">
          <div class="form-hint">Telefonska številka bo potrebna za WhatsApp obvestila.</div></div>
      </div>
      <div id="s-manager-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-manager-save">Shrani</button></div>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Podatki organizacije</h2>
      <div class="field"><label>Naziv organizacije</label>
        <input id="s-ngo-name" type="text" value="${esc(manager.ngo_name)}" required maxlength="200"></div>
      <div class="field"><label>Ulica in hišna številka</label>
        <input id="s-ngo-street" type="text" value="${esc(manager.ngo_street)}" required maxlength="255"></div>
      <div class="form-row">
        <div class="field"><label>Poštna številka</label>
          <input id="s-ngo-postal" type="text" value="${esc(manager.ngo_postal_code)}" required pattern="\\d{4}" maxlength="4"></div>
        <div class="field"><label>Kraj</label>
          <input id="s-ngo-city" type="text" value="${esc(manager.ngo_city)}" required maxlength="100"></div>
      </div>
      <div class="field" style="margin-top:0.75rem">
        <label>Davčna številka organizacije</label>
        <input id="s-ngo-davcna" type="text" inputmode="numeric" value="${esc(manager.ngo_davcna || '')}" maxlength="8" placeholder="12345678" style="max-width:10rem">
        <div class="form-hint">8 številk brez presledkov ali črk.</div>
      </div>
      <div class="field" style="margin-top:0.75rem">
        <label>Mobilna številka za BelPro</label>
        <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
          <input id="s-ngo-wa-phone" type="tel"
            value="${esc(configInfo.wa_phone ? '+' + configInfo.wa_phone : (manager.ngo_whatsapp_phone ? '+' + manager.ngo_whatsapp_phone : ''))}"
            maxlength="30" placeholder="+38640..."
            ${(configInfo.wa_state === 'open' || configInfo.wa_state === 'connecting') ? 'readonly' : ''}>
          ${_waBadge(configInfo.wa_state)}
        </div>
        ${(configInfo.wa_state === 'open' || configInfo.wa_state === 'connecting')
          ? '<div class="form-hint">Številko upravljate prek <a href="https://evoapicloud.com/" target="_blank" rel="noopener noreferrer"><img src="/images/evolution-api-logo.svg" alt="Evolution API" style="height:1.8em;vertical-align:middle;border-radius:3px;background:#111;padding:0 3px;"></a> — spremenite jo na spodnji povezavi in nato osvežite to stran.</div>'
          : '<div class="form-hint">Telefonska številka, ki je povezana z WhatsApp botom (<a href="https://evoapicloud.com/" target="_blank" rel="noopener noreferrer"><img src="/images/evolution-api-logo.svg" alt="Evolution API" style="height:1.8em;vertical-align:middle;border-radius:3px;background:#111;padding:0 3px;"></a>).</div>'}
      </div>
      <div style="margin-top:0.5rem">
        <a id="s-evo-api-link" href="${esc(configInfo.evolution_api_admin_url)}" target="_blank" rel="noopener noreferrer"
           class="btn btn-secondary btn-sm">Odpri nastavitve Evolution API ↗</a>
      </div>
      <div id="s-ngo-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-ngo-save">Shrani</button></div>
    </div>

    <div style="${card}">
      <h2 style="${h2}">E-poštna integracija</h2>
      <div class="form-row">
        <div class="field"><label>SMTP strežnik</label>
          <input id="s-smtp-host" type="text" value="${esc(configInfo.smtp_host)}" maxlength="255" placeholder="smtp.gmail.com"></div>
        <div class="field"><label>Vrata</label>
          <input id="s-smtp-port" type="number" value="${configInfo.smtp_port || 587}" min="1" max="65535" style="max-width:7rem"></div>
      </div>
      <div class="form-row">
        <div class="field"><label>Uporabniško ime (e-naslov)</label>
          <input id="s-smtp-user" type="email" value="${esc(configInfo.smtp_user)}" maxlength="255" placeholder="ngo@example.com"></div>
        <div class="field"><label>Ime pošiljatelja</label>
          <input id="s-smtp-from" type="text" value="${esc(configInfo.smtp_from_name)}" maxlength="100" placeholder="${esc(manager.ngo_name)}"></div>
      </div>
      <div style="margin-top:0.25rem;margin-bottom:0.75rem">
        ${configInfo.smtp_configured
          ? '<span style="color:var(--success,#16a34a);font-size:0.85rem">✓ E-pošta je konfigurirana</span>'
          : '<span style="color:var(--text-muted,#6b7280);font-size:0.85rem">Ni konfigurirano — geslo nastavite v <code>.env</code> (SMTP_PASSWORD)</span>'}
      </div>
      <div class="form-hint" style="margin-bottom:0.75rem">Geslo SMTP ostane v <code>.env</code> datoteki in se ne shranjuje v bazi.
        Za Gmail uporabite <a href="https://accounts.google.com/AccountChooser?continue=https://myaccount.google.com/apppasswords" target="_blank" rel="noopener noreferrer">geslo aplikacije ↗</a>
        (odpre izbiro Google računa, nato gesla aplikacij).</div>
      <div id="s-smtp-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-smtp-save">Shrani</button></div>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Moja mesečna poročila</h2>
      <p class="form-hint">Kako želite prejemati mesečno konsolidirano poročilo?</p>
      <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
        <input type="checkbox" id="s-my-rp-master" ${(manager.report_email || manager.report_whatsapp) ? 'checked' : ''}>
        <span>Pošiljanje mesečnih poročil</span>
      </label>
      <div id="s-my-rp-sub" style="margin-left:1.5rem;margin-top:0.5rem;display:flex;flex-direction:column;gap:0.4rem">
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="s-my-rp-email" ${manager.report_email ? 'checked' : ''}> E-pošta
        </label>
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="s-my-rp-whatsapp" ${manager.report_whatsapp ? 'checked' : ''}> WhatsApp
        </label>
      </div>
      <div id="s-my-rp-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-my-rp-save">Shrani</button></div>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Privzete nastavitve poročil za prostovoljce</h2>
      <p class="form-hint">Te nastavitve se uporabijo pri registraciji novega prostovoljca.</p>
      <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
        <input type="checkbox" id="s-def-rp-master" ${(manager.default_report_email || manager.default_report_whatsapp) ? 'checked' : ''}>
        <span>Pošiljanje mesečnih poročil</span>
      </label>
      <div id="s-def-rp-sub" style="margin-left:1.5rem;margin-top:0.5rem;display:flex;flex-direction:column;gap:0.4rem">
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="s-def-rp-email" ${manager.default_report_email ? 'checked' : ''}> E-pošta
        </label>
        <label class="checkbox-label" style="display:flex;align-items:center;gap:0.5rem;cursor:pointer">
          <input type="checkbox" id="s-def-rp-whatsapp" ${manager.default_report_whatsapp ? 'checked' : ''}> WhatsApp
        </label>
      </div>
      <div id="s-def-rp-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-def-rp-save">Shrani</button></div>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Sprememba gesla</h2>
      <div class="field"><label>Trenutno geslo</label>
        <input id="s-cur-pass" type="password" autocomplete="current-password"></div>
      <div class="form-row">
        <div class="field"><label>Novo geslo</label>
          <input id="s-new-pass" type="password" autocomplete="new-password" minlength="8">
          <div class="form-hint">Vsaj 8 znakov.</div></div>
        <div class="field"><label>Ponovi novo geslo</label>
          <input id="s-new-pass2" type="password" autocomplete="new-password"></div>
      </div>
      <div id="s-pass-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-pass-save">Shrani</button></div>
    </div>
  `);

  function showErr(id, msg) {
    const el = $(id);
    el.textContent = msg;
    el.style.display = msg ? '' : 'none';
  }

  $('s-manager-save').addEventListener('click', async () => {
    showErr('s-manager-error', '');
    const payload = {
      first_name: $('s-first-name').value.trim(),
      last_name:  $('s-last-name').value.trim(),
      email:      $('s-email').value.trim(),
      phone:      $('s-phone').value.trim(),
    };
    if (!payload.first_name || !payload.last_name || !payload.email || !payload.phone) {
      showErr('s-manager-error', 'Vsa polja so obvezna.'); return;
    }
    try {
      await API.managers.update(payload);
      toast('Podatki upravljalca so bili shranjeni.');
    } catch (err) {
      showErr('s-manager-error', err.message);
    }
  });

  $('s-ngo-save').addEventListener('click', async () => {
    showErr('s-ngo-error', '');
    const payload = {
      ngo_name:           $('s-ngo-name').value.trim(),
      ngo_street:         $('s-ngo-street').value.trim(),
      ngo_postal_code:    $('s-ngo-postal').value.trim(),
      ngo_city:           $('s-ngo-city').value.trim(),
      ngo_davcna:         $('s-ngo-davcna').value.trim() || null,
      ngo_whatsapp_phone: $('s-ngo-wa-phone').value.trim() || null,
    };
    if (!payload.ngo_name || !payload.ngo_street || !payload.ngo_postal_code || !payload.ngo_city) {
      showErr('s-ngo-error', 'Polja naziv, ulica, poštna številka in kraj so obvezna.'); return;
    }
    if (!/^\d{4}$/.test(payload.ngo_postal_code)) {
      showErr('s-ngo-error', 'Poštna številka mora biti 4-mestna številka.'); return;
    }
    if (payload.ngo_davcna) {
      if (!/^\d{8}$/.test(payload.ngo_davcna)) {
        showErr('s-ngo-error', 'Davčna številka mora vsebovati natanko 8 številk.'); return;
      }
      if (!_davcnaValid(payload.ngo_davcna)) {
        showErr('s-ngo-error', 'Davčna številka je neveljavna (napačna kontrolna številka).'); return;
      }
    }
    try {
      await API.managers.update(payload);
      const evoLink = $('s-evo-api-link');
      if (evoLink) evoLink.href = configInfo.evolution_api_admin_url;
      toast('Podatki organizacije so bili shranjeni.');
    } catch (err) {
      showErr('s-ngo-error', err.message);
    }
  });

  $('s-smtp-save').addEventListener('click', async () => {
    showErr('s-smtp-error', '');
    const port = parseInt($('s-smtp-port').value, 10);
    if ($('s-smtp-host').value.trim() && (isNaN(port) || port < 1 || port > 65535)) {
      showErr('s-smtp-error', 'Vrata morajo biti številka med 1 in 65535.'); return;
    }
    const payload = {
      smtp_host:      $('s-smtp-host').value.trim() || null,
      smtp_port:      isNaN(port) ? null : port,
      smtp_user:      $('s-smtp-user').value.trim() || null,
      smtp_from_name: $('s-smtp-from').value.trim() || null,
    };
    try {
      await API.managers.update(payload);
      toast('Nastavitve e-pošte so bile shranjene.');
    } catch (err) {
      showErr('s-smtp-error', err.message);
    }
  });

  $('s-pass-save').addEventListener('click', async () => {
    showErr('s-pass-error', '');
    const cur  = $('s-cur-pass').value;
    const nw   = $('s-new-pass').value;
    const nw2  = $('s-new-pass2').value;
    if (!cur || !nw || !nw2) {
      showErr('s-pass-error', 'Vsa polja so obvezna.'); return;
    }
    if (nw.length < 8) {
      showErr('s-pass-error', 'Novo geslo mora imeti vsaj 8 znakov.'); return;
    }
    if (nw !== nw2) {
      showErr('s-pass-error', 'Novi gesli se ne ujemata.'); return;
    }
    try {
      await API.managers.changePassword({ current_password: cur, new_password: nw });
      API.setPassword(nw);
      $('s-cur-pass').value = '';
      $('s-new-pass').value = '';
      $('s-new-pass2').value = '';
      toast('Geslo je bilo uspešno spremenjeno.');
    } catch (err) {
      showErr('s-pass-error', err.message);
    }
  });

  wireReportPrefs(
    $('s-my-rp-master'), $('s-my-rp-email'), $('s-my-rp-whatsapp'),
    $('s-my-rp-error'),
    async (wa, email) => {
      await API.managers.update({ report_whatsapp: wa, report_email: email });
      toast('Nastavitve mojih poročil so bile shranjene.');
    }
  );

  wireReportPrefs(
    $('s-def-rp-master'), $('s-def-rp-email'), $('s-def-rp-whatsapp'),
    $('s-def-rp-error'),
    async (wa, email) => {
      await API.managers.update({ default_report_whatsapp: wa, default_report_email: email });
      toast('Privzete nastavitve poročil so bile shranjene.');
    }
  );
}

// ===== Approvals page =====
function approvalsSortTh(label, col) {
  const active = approvalsState.filter.sort_by === col ? ' sort-active' : '';
  const arrow  = approvalsState.filter.sort_by === col
    ? (approvalsState.filter.sort_dir === 'asc' ? '↑' : '↓')
    : '↕';
  return `<th class="sortable${active}" data-sort="${col}">${esc(label)} <span class="sort-arrow">${arrow}</span></th>`;
}

function renderApprovalsThead() {
  return `
    ${approvalsSortTh('Datum dela', 'work_date')}
    <th>Prostovoljec</th>
    ${approvalsSortTh('Opis dela', 'activity_description')}
    ${approvalsSortTh('Ure', 'hours')}
    ${approvalsSortTh('Lokacija', 'location')}
    ${approvalsSortTh('Dan vnosa', 'created_at')}
    <th>Status</th>
    <th>Dejanja</th>
  `;
}

function renderApprovalsTable() {
  const tbody = $('approvals-body');
  if (!tbody) return;

  const { items, filter, volunteerMap } = approvalsState;

  if (!items.length) {
    const msg = filter.status === 'pending_manager'
      ? 'Ni čakajočih vnosov.'
      : 'Ni vnosov, ki ustrezajo filtru.';
    setHtml(tbody, `<tr class="empty-row"><td colspan="8">${msg}</td></tr>`);
    return;
  }

  tbody.innerHTML = items.map(e => {
    const name = volunteerMap.get(e.volunteer_id) || 'Neznano';
    const desc = e.activity_description.length > 60
      ? esc(e.activity_description.slice(0, 60)) + '…'
      : esc(e.activity_description);
    const actions = e.status === 'pending_manager'
      ? `<button class="btn btn-sm btn-primary" data-action="approve" data-id="${e.id}">Odobri</button>
         <button class="btn btn-sm btn-danger"  data-action="reject"  data-id="${e.id}" style="margin-left:0.4rem">Zavrni</button>`
      : '';
    return `
      <tr data-id="${e.id}" style="cursor:pointer">
        <td>${esc(e.work_date)}</td>
        <td data-stop><a href="#approvals/volunteer/${e.volunteer_id}" style="color:var(--accent);text-decoration:none">${esc(name)}</a></td>
        <td>${desc}</td>
        <td style="text-align:right">${fmtHours(e.hours)}</td>
        <td>${e.location ? esc(e.location) : '—'}</td>
        <td>${e.created_at.slice(0, 10)}</td>
        <td>${statusBadge(e.status)}</td>
        <td class="td-actions" data-stop>${actions}</td>
      </tr>`;
  }).join('');
}

function renderApprovalsPagination() {
  const { filter, total } = approvalsState;
  const from    = total === 0 ? 0 : filter.offset + 1;
  const to      = Math.min(filter.offset + filter.limit, total);
  const info    = $('a-pg-info');
  const prevBtn = $('a-prev-btn');
  const nextBtn = $('a-next-btn');
  if (info)    info.textContent = total > 0 ? `Prikazujem ${from}–${to} od ${total}` : 'Ni rezultatov';
  if (prevBtn) prevBtn.disabled = filter.offset === 0;
  if (nextBtn) nextBtn.disabled = filter.offset + filter.limit >= total;
}

async function loadApprovals() {
  const tbody = $('approvals-body');
  if (!tbody) return;

  const { filter } = approvalsState;
  const params = {
    sort_by:  filter.sort_by,
    sort_dir: filter.sort_dir,
    offset:   filter.offset,
    limit:    filter.limit,
  };
  if (filter.status)    params.status    = filter.status;
  if (filter.search_q)  params.search_q  = filter.search_q;
  if (filter.date_from) params.date_from = filter.date_from;
  if (filter.date_to)   params.date_to   = filter.date_to;
  if (filter.date_from || filter.date_to) params.date_field = filter.date_field;

  try {
    const data = await API.logEntries.list(params);
    approvalsState.total = data.total;
    approvalsState.items = data.items;
    const head = $('approvals-head');
    if (head) setHtml(head, renderApprovalsThead());
    renderApprovalsTable();
    renderApprovalsPagination();
  } catch (err) {
    setHtml(tbody, `<tr class="empty-row"><td colspan="7">Napaka: ${esc(err.message)}</td></tr>`);
  }
}

// ===== Volunteer Log (detail page) =====

function volLogSortTh(label, col) {
  const active = volunteerLogState.filter.sort_by === col ? ' sort-active' : '';
  const arrow  = volunteerLogState.filter.sort_by === col
    ? (volunteerLogState.filter.sort_dir === 'asc' ? '↑' : '↓')
    : '↕';
  return `<th class="sortable${active}" data-sort="${col}">${esc(label)} <span class="sort-arrow">${arrow}</span></th>`;
}

function renderVolunteerLogThead() {
  return `
    ${volLogSortTh('Datum dela', 'work_date')}
    ${volLogSortTh('Opis dela', 'activity_description')}
    ${volLogSortTh('Ure', 'hours')}
    ${volLogSortTh('Lokacija', 'location')}
    ${volLogSortTh('Dan vnosa', 'created_at')}
    <th>Status</th>
  `;
}

function renderVolunteerLogTable() {
  const tbody = $('vlog-body');
  if (!tbody) return;

  const { items } = volunteerLogState;

  if (!items.length) {
    setHtml(tbody, `<tr class="empty-row"><td colspan="6">Ni vnosov, ki ustrezajo filtru.</td></tr>`);
    return;
  }

  tbody.innerHTML = items.map(e => {
    const desc = e.activity_description.length > 60
      ? esc(e.activity_description.slice(0, 60)) + '…'
      : esc(e.activity_description);
    return `
      <tr data-id="${e.id}" style="cursor:pointer">
        <td>${esc(e.work_date)}</td>
        <td>${desc}</td>
        <td style="text-align:right">${fmtHours(e.hours)}</td>
        <td>${e.location ? esc(e.location) : '—'}</td>
        <td>${e.created_at.slice(0, 10)}</td>
        <td>${statusBadge(e.status)}</td>
      </tr>`;
  }).join('');
}

function renderVolunteerLogPagination() {
  const { filter, total } = volunteerLogState;
  const from    = total === 0 ? 0 : filter.offset + 1;
  const to      = Math.min(filter.offset + filter.limit, total);
  const info    = $('vlog-pg-info');
  const prevBtn = $('vlog-prev-btn');
  const nextBtn = $('vlog-next-btn');
  if (info)    info.textContent = total > 0 ? `Prikazujem ${from}–${to} od ${total}` : 'Ni rezultatov';
  if (prevBtn) prevBtn.disabled = filter.offset === 0;
  if (nextBtn) nextBtn.disabled = filter.offset + filter.limit >= total;
}

async function loadVolunteerLog() {
  const tbody = $('vlog-body');
  if (!tbody) return;

  const { volunteerId, filter } = volunteerLogState;
  const params = {
    volunteer_id: volunteerId,
    sort_by:      filter.sort_by,
    sort_dir:     filter.sort_dir,
    offset:       filter.offset,
    limit:        filter.limit,
  };
  if (filter.status)    params.status    = filter.status;
  if (filter.search_q)  params.search_q  = filter.search_q;
  if (filter.date_from) params.date_from = filter.date_from;
  if (filter.date_to)   params.date_to   = filter.date_to;
  if (filter.date_from || filter.date_to) params.date_field = filter.date_field;

  try {
    const data = await API.logEntries.list(params);
    volunteerLogState.total = data.total;
    volunteerLogState.items = data.items;
    const head = $('vlog-head');
    if (head) setHtml(head, renderVolunteerLogThead());
    renderVolunteerLogTable();
    renderVolunteerLogPagination();
  } catch (err) {
    setHtml(tbody, `<tr class="empty-row"><td colspan="5">Napaka: ${esc(err.message)}</td></tr>`);
  }
}

async function renderApprovals() {
  $('topbar-title').textContent = 'Dnevniki';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="approvals"]')?.classList.add('active');

  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  try {
    const volData = await API.volunteers.list({ limit: 200 });
    approvalsState.volunteerMap = new Map(volData.items.map(v => [v.id, v.first_name + ' ' + v.last_name]));
  } catch {
    approvalsState.volunteerMap = new Map();
  }

  const statusOpt = (val, label) => {
    const sel = approvalsState.filter.status === val ? ' selected' : '';
    return `<option value="${val}"${sel}>${label}</option>`;
  };

  setHtml($('main-content'), `
    <div class="page-header">
      <div>
        <h1 class="page-title">Dnevniki</h1>
        <p class="page-subtitle">Dnevniški zapisi</p>
      </div>
    </div>

    <div class="filter-bar">
      <select id="a-status">
        ${statusOpt('pending_manager', 'Čaka odobritev')}
        ${statusOpt('approved',        'Odobreno')}
        ${statusOpt('rejected',        'Zavrnjeno')}
        ${statusOpt('',               'Vsi')}
      </select>
      <label style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center;display:flex;align-items:center;gap:0.3rem;cursor:pointer">
        <input type="checkbox" id="a-date-field-cb" ${approvalsState.filter.date_field === 'created_at' ? 'checked' : ''} />
        Dan vnosa
      </label>
      <label for="a-date-from" style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center">Od:</label>
      <input type="date" id="a-date-from" value="${approvalsState.filter.date_from || ''}" />
      <label for="a-date-to" style="font-size:0.8rem;color:var(--text-muted);white-space:nowrap;align-self:center">Do:</label>
      <input type="date" id="a-date-to" value="${approvalsState.filter.date_to || ''}" />
      <input type="text" id="a-search-q" placeholder="Iskanje po opisu ali lokaciji…"
             value="${esc(approvalsState.filter.search_q)}" style="flex:1;min-width:130px;max-width:280px" />
      <button class="btn btn-primary btn-sm" id="a-search">Išči</button>
      <button class="btn btn-ghost btn-sm" id="a-reset">Ponastavi</button>
    </div>

    <div class="table-wrapper">
      <table id="approvals-table">
        <thead><tr id="approvals-head">${renderApprovalsThead()}</tr></thead>
        <tbody id="approvals-body"><tr class="loading-row"><td colspan="7">Nalaganje…</td></tr></tbody>
      </table>
    </div>

    <div class="pagination">
      <span id="a-pg-info"></span>
      <div class="pagination-btns">
        <button id="a-prev-btn" disabled>← Prejšnja</button>
        <button id="a-next-btn" disabled>Naslednja →</button>
      </div>
    </div>
  `);

  $('a-status').addEventListener('change', () => {
    approvalsState.filter.status = $('a-status').value;
    approvalsState.filter.offset = 0;
    loadApprovals();
  });

  function applyApprovalsSearch() {
    approvalsState.filter.search_q = $('a-search-q')?.value.trim() || '';
    approvalsState.filter.offset = 0;
    loadApprovals();
  }

  $('a-search').addEventListener('click', applyApprovalsSearch);
  $('a-search-q').addEventListener('keydown', e => { if (e.key === 'Enter') applyApprovalsSearch(); });

  $('a-date-field-cb').addEventListener('change', () => {
    approvalsState.filter.date_field = $('a-date-field-cb').checked ? 'created_at' : 'work_date';
    approvalsState.filter.offset = 0;
    loadApprovals();
  });
  $('a-date-from').addEventListener('change', () => {
    approvalsState.filter.date_from = $('a-date-from').value || null;
    approvalsState.filter.offset = 0;
    loadApprovals();
  });
  $('a-date-to').addEventListener('change', () => {
    approvalsState.filter.date_to = $('a-date-to').value || null;
    approvalsState.filter.offset = 0;
    loadApprovals();
  });

  $('a-reset').addEventListener('click', () => {
    approvalsState.filter.search_q  = '';
    approvalsState.filter.date_from = null;
    approvalsState.filter.date_to   = null;
    approvalsState.filter.date_field = 'work_date';
    $('a-search-q').value       = '';
    $('a-date-from').value      = '';
    $('a-date-to').value        = '';
    $('a-date-field-cb').checked = false;
    approvalsState.filter.offset = 0;
    loadApprovals();
  });

  $('a-prev-btn').addEventListener('click', () => {
    approvalsState.filter.offset = Math.max(0, approvalsState.filter.offset - approvalsState.filter.limit);
    loadApprovals();
  });

  $('a-next-btn').addEventListener('click', () => {
    approvalsState.filter.offset += approvalsState.filter.limit;
    loadApprovals();
  });

  $('approvals-table').addEventListener('click', async (e) => {
    const th = e.target.closest('th[data-sort]');
    if (th) {
      const col = th.dataset.sort;
      if (approvalsState.filter.sort_by === col) {
        approvalsState.filter.sort_dir = approvalsState.filter.sort_dir === 'asc' ? 'desc' : 'asc';
      } else {
        approvalsState.filter.sort_by  = col;
        approvalsState.filter.sort_dir = 'asc';
      }
      approvalsState.filter.offset = 0;
      await loadApprovals();
      return;
    }

    const row = e.target.closest('tr[data-id]');
    if (row && !e.target.closest('[data-stop]')) {
      location.hash = '#approvals/' + row.dataset.id;
      return;
    }

    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const { action, id } = btn.dataset;
    btn.disabled = true;
    btn.textContent = '…';
    try {
      if (action === 'approve') {
        await API.logEntries.approve(id);
        toast('Vnos odobren.');
      } else if (action === 'reject') {
        await API.logEntries.reject(id);
        toast('Vnos zavrnjen.', 'error');
      }
      await loadApprovals();
    } catch (err) {
      toast('Napaka: ' + err.message, 'error');
      btn.disabled = false;
      btn.textContent = action === 'approve' ? 'Odobri' : 'Zavrni';
    }
  });

  await loadApprovals();
}

function formatExifCaption(p) {
  const parts = [];
  if (p.photo_exif_lat != null && p.photo_exif_lon != null)
    parts.push(`<a href="https://maps.google.com/?q=${p.photo_exif_lat},${p.photo_exif_lon}" target="_blank" rel="noopener noreferrer" style="color:var(--primary);text-decoration:none">Lokacija</a>`);
  if (p.photo_exif_timestamp)
    parts.push(p.photo_exif_timestamp.slice(0, 16).replace('T', ' '));
  return parts.length
    ? `<div style="font-size:0.7rem;color:var(--text-muted);max-width:130px;margin-top:3px;line-height:1.4">${parts.join('<br>')}</div>`
    : '';
}

// ===== Log entry detail =====
async function renderLogEntryDetail(id, { backHash = '#approvals', backLabel = '← Nazaj na dnevnike', backNav = 'approvals', goBack = null } = {}) {
  revokePhotoUrls();
  $('topbar-title').textContent = 'Vnos';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector(`[data-page="${backNav}"]`)?.classList.add('active');
  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  let entry, volName;
  try {
    entry = await API.logEntries.get(id);
    const vol = await API.volunteers.get(entry.volunteer_id);
    volName = vol.first_name + ' ' + vol.last_name;
  } catch (err) {
    setHtml($('main-content'), `<p style="color:var(--danger);padding:1rem">Napaka: ${esc(err.message)}</p>`);
    return;
  }

  const BLANK      = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';
  const editable   = entry.status !== 'approved';
  const canApprove = entry.status === 'pending_manager';
  const tileStyle  = 'position:relative;width:130px;height:130px;background:var(--border);border-radius:var(--radius);overflow:hidden;cursor:pointer';
  const delStyle   = 'position:absolute;top:4px;right:4px;width:26px;height:26px;background:rgba(0,0,0,0.55);color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:18px;line-height:26px;text-align:center;padding:0';
  const phStyle    = 'width:130px;height:130px;background:var(--border);border-radius:var(--radius);opacity:0.35;flex-shrink:0';

  const photoTiles = entry.photos.length > 0
    ? entry.photos.map(p => `
        <div data-photo-id="${p.id}" style="display:flex;flex-direction:column;flex-shrink:0">
          <div class="photo-tile" style="${tileStyle}">
            <img data-photo-id="${p.id}" src="${BLANK}" alt="Fotografija"
                 style="width:100%;height:100%;object-fit:cover;display:block" />
            ${editable ? `<button class="photo-del-btn" data-photo-id="${p.id}" style="${delStyle}" title="Izbriši">×</button>` : ''}
          </div>${formatExifCaption(p)}
        </div>`).join('')
    : `<div data-placeholder style="${phStyle}"></div><div data-placeholder style="${phStyle}"></div>`;

  const addTile = editable ? `
    <label for="photo-upload"
           style="width:130px;height:130px;border:2px dashed var(--border);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text-muted);font-size:2.5rem;flex-shrink:0"
           title="Dodaj fotografijo">+</label>
    <input type="file" id="photo-upload" accept="image/*" multiple style="display:none" />` : '';

  setHtml($('main-content'), `
    <button class="back-link" id="back-btn">${backLabel}</button>

    <div class="detail-header">
      <div>
        <div class="detail-name">${esc(entry.work_date)}</div>
        <div style="margin-top:0.4rem">${statusBadge(entry.status)}</div>
      </div>
      ${canApprove ? `
        <div style="display:flex;gap:0.5rem;align-items:center">
          <button class="btn btn-primary btn-sm" id="approve-btn">Odobri</button>
          <button class="btn btn-danger btn-sm"  id="reject-btn">Zavrni</button>
        </div>` : ''}
    </div>

    <div class="detail-info-grid">
      <div class="info-item">
        <div class="info-label">Datum dela</div>
        <div class="info-value">${esc(entry.work_date)}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Prostovoljec</div>
        <div class="info-value"><a href="${backNav === 'approvals' ? `#approvals/${id}/volunteer/${entry.volunteer_id}` : `#volunteers/${entry.volunteer_id}`}" style="color:var(--accent)">${esc(volName)}</a></div>
      </div>
      <div class="info-item">
        <div class="info-label">Ure</div>
        <div class="info-value" id="d-hours-display">${fmtHours(entry.hours)}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Lokacija</div>
        <div class="info-value">${entry.location ? esc(entry.location) : '—'}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Ustvarjeno</div>
        <div class="info-value">${fmtDatetime(entry.created_at)}</div>
      </div>
      ${entry.manager_approved_at ? `
        <div class="info-item">
          <div class="info-label">${entry.status === 'approved' ? 'Odobreno' : 'Zavrnjeno'}</div>
          <div class="info-value">${fmtDatetime(entry.manager_approved_at)}</div>
        </div>` : ''}
    </div>

    <p class="section-title">Opis dela</p>
    <div id="d-desc-display" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;white-space:pre-wrap;line-height:1.6;margin-bottom:1.5rem">${esc(entry.activity_description)}</div>

    ${entry.raw_transcript ? `
      <p class="section-title">Prepis (glasovni vnos)</p>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;white-space:pre-wrap;line-height:1.6;color:var(--text-muted);font-size:0.88rem;margin-bottom:1.5rem">${esc(entry.raw_transcript)}</div>
    ` : ''}

    <p class="section-title">Fotografije</p>
    <div id="photo-grid" style="display:flex;flex-wrap:wrap;gap:0.75rem;margin-bottom:1.5rem">
      ${photoTiles}${addTile}
    </div>

    ${editable ? `
      <p class="section-title">Uredi vnos</p>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem">
        <div class="field">
          <label>Opis dela</label>
          <textarea id="d-desc" rows="4" style="width:100%;resize:vertical">${esc(entry.activity_description)}</textarea>
        </div>
        <div class="field" style="max-width:160px">
          <label>Ure</label>
          <input type="number" id="d-hours" value="${entry.hours}" min="0.5" max="24" step="0.5" />
        </div>
        <div class="field" style="max-width:200px">
          <label>Datum dela</label>
          <input type="date" id="d-work-date" value="${entry.work_date}" />
        </div>
        <div class="field">
          <label>Lokacija</label>
          <input type="text" id="d-location" value="${esc(entry.location || '')}" placeholder="Npr. Dom starejših Trnovo" />
        </div>
        <div id="d-edit-error" class="form-error" hidden></div>
        <div class="form-actions">
          <button class="btn btn-primary btn-sm" id="d-save-btn">Shrani spremembe</button>
        </div>
      </div>
    ` : ''}
  `);

  // Load photo blobs asynchronously — non-blocking
  entry.photos.forEach(async (p) => {
    const img = document.querySelector(`img[data-photo-id="${p.id}"]`);
    if (!img) return;
    const url = await API.logEntries.photoUrl(entry.id, p.id);
    if (url) { _photoObjectUrls.push(url); img.src = url; }
  });

  // Photo grid click: delete or enlarge
  const grid = $('photo-grid');
  grid?.addEventListener('click', async (e) => {
    const delBtn = e.target.closest('.photo-del-btn');
    if (delBtn) {
      e.stopPropagation();
      if (!editable) return;
      const pid = delBtn.dataset.photoId;
      if (!confirm('Izbriši fotografijo?')) return;
      delBtn.disabled = true;
      try {
        await API.logEntries.deletePhoto(entry.id, pid);
        grid.querySelector(`[data-photo-id="${pid}"]`)?.remove();
        entry.photos = entry.photos.filter(p => p.id !== pid);
        if (entry.photos.length === 0) {
          const ph = `<div data-placeholder style="${phStyle}"></div>`;
          const addLabel = grid.querySelector('label[for="photo-upload"]');
          addLabel
            ? addLabel.insertAdjacentHTML('beforebegin', ph + ph)
            : grid.insertAdjacentHTML('afterbegin', ph + ph);
        }
        toast('Fotografija izbrisana.');
      } catch (err) {
        toast('Napaka: ' + err.message, 'error');
        delBtn.disabled = false;
      }
      return;
    }

    const tile = e.target.closest('.photo-tile');
    if (tile) {
      const img = tile.querySelector('img');
      if (img?.src.startsWith('blob:')) {
        openModal('Fotografija', `<img src="${img.src}" style="max-width:100%;max-height:75vh;display:block;margin:auto;border-radius:var(--radius)" />`);
      }
    }
  });

  // Upload
  $('photo-upload')?.addEventListener('change', async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    const addLabel = grid?.querySelector('label[for="photo-upload"]');
    for (const file of files) {
      const fd = new FormData();
      fd.append('file', file);
      try {
        const photo = await API.logEntries.uploadPhoto(entry.id, fd);
        entry.photos.push(photo);
        grid?.querySelectorAll('[data-placeholder]').forEach(el => el.remove());
        const tileHtml = `
          <div data-photo-id="${photo.id}" style="display:flex;flex-direction:column;flex-shrink:0">
            <div class="photo-tile" style="${tileStyle}">
              <img data-photo-id="${photo.id}" src="${BLANK}" alt="Fotografija"
                   style="width:100%;height:100%;object-fit:cover;display:block" />
              <button class="photo-del-btn" data-photo-id="${photo.id}" style="${delStyle}" title="Izbriši">×</button>
            </div>${formatExifCaption(photo)}
          </div>`;
        addLabel
          ? addLabel.insertAdjacentHTML('beforebegin', tileHtml)
          : grid?.insertAdjacentHTML('beforeend', tileHtml);
        const url = await API.logEntries.photoUrl(entry.id, photo.id);
        if (url) {
          _photoObjectUrls.push(url);
          const img = document.querySelector(`img[data-photo-id="${photo.id}"]`);
          if (img) img.src = url;
        }
        toast('Fotografija naložena.');
      } catch (err) {
        toast('Napaka: ' + err.message, 'error');
      }
    }
    e.target.value = '';
  });

  $('back-btn').addEventListener('click', () => {
    revokePhotoUrls();
    history.pushState(null, '', backHash);
    (goBack || renderApprovals)();
  });

  if (canApprove) {
    const doAction = async (action) => {
      const btn = $(action === 'approve' ? 'approve-btn' : 'reject-btn');
      btn.disabled = true;
      btn.textContent = '…';
      try {
        if (action === 'approve') {
          await API.logEntries.approve(entry.id);
          toast('Vnos odobren.');
        } else {
          await API.logEntries.reject(entry.id);
          toast('Vnos zavrnjen.', 'error');
        }
        revokePhotoUrls();
        history.pushState(null, '', backHash);
        (goBack || renderApprovals)();
      } catch (err) {
        toast('Napaka: ' + err.message, 'error');
        btn.disabled = false;
        btn.textContent = action === 'approve' ? 'Odobri' : 'Zavrni';
      }
    };
    $('approve-btn').addEventListener('click', () => doAction('approve'));
    $('reject-btn').addEventListener('click',  () => doAction('reject'));
  }

  if (editable) {
    $('d-save-btn').addEventListener('click', async () => {
      const desc     = $('d-desc').value.trim();
      const hours    = parseFloat($('d-hours').value);
      const workDate = $('d-work-date').value;
      const errEl    = $('d-edit-error');
      if (!desc) {
        errEl.textContent = 'Opis dela ne sme biti prazen.';
        errEl.hidden = false;
        return;
      }
      if (isNaN(hours) || hours < 0.5 || hours > 24) {
        errEl.textContent = 'Ure morajo biti med 0.5 in 24.';
        errEl.hidden = false;
        return;
      }
      if (!workDate) {
        errEl.textContent = 'Dan opravljenega dela je obvezen.';
        errEl.hidden = false;
        return;
      }
      errEl.hidden = true;
      $('d-save-btn').disabled = true;
      $('d-save-btn').textContent = 'Shranjevanje…';
      const location = $('d-location').value.trim() || null;
      try {
        await API.logEntries.update(entry.id, { activity_description: desc, hours, location, work_date: workDate });
        toast('Vnos posodobljen.');
        await renderLogEntryDetail(id, { backHash, backLabel, backNav, goBack });
      } catch (err) {
        errEl.textContent = err.message;
        errEl.hidden = false;
        $('d-save-btn').disabled = false;
        $('d-save-btn').textContent = 'Shrani spremembe';
      }
    });
  }
}

// ===== Init =====
(async function init() {
  if (API.loadFromSession()) {
    try {
      await API.health();
      showApp();
      await checkManagerSetup();
    } catch {
      API.clear();
      showLogin();
    }
  } else {
    showLogin();
  }
}());
