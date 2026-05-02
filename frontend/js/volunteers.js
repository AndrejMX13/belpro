'use strict';

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
      && e.target !== $('hamburger')) {
    _sidebar.classList.remove('open');
  }
});

document.querySelectorAll('.nav-item[data-page]').forEach(link => {
  link.addEventListener('click', () => _sidebar.classList.remove('open'));
});

// ===== Router =====
function route() {
  const hash = location.hash || '#volunteers';
  if (hash.startsWith('#volunteers/')) {
    renderDetail(hash.slice('#volunteers/'.length));
  } else if (hash.startsWith('#approvals/')) {
    renderLogEntryDetail(hash.slice('#approvals/'.length));
  } else if (hash === '#approvals') {
    renderApprovals();
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
  filter: { status: 'pending_manager', search_q: '', date_from: null, date_to: null, sort_by: 'entry_date', sort_dir: 'desc', offset: 0, limit: 20 },
  total: 0,
  items: [],
  volunteerMap: new Map(),
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
function openAddModal() {
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
      <div id="add-error" class="form-error" hidden></div>
      <div class="form-actions">
        <button type="button" class="btn btn-ghost" id="cancel-add">Prekliči</button>
        <button type="submit" class="btn btn-primary" id="add-submit">Shrani</button>
      </div>
    </form>
  `);

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
async function renderDetail(id) {
  $('topbar-title').textContent = 'Prostovoljec';
  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  try {
    const v = await API.volunteers.get(id);
    const initials = (v.first_name[0] + v.last_name[0]).toUpperCase();

    const entriesRows = v.log_entries.length === 0
      ? '<tr class="empty-row"><td colspan="5">Ni vnosov.</td></tr>'
      : v.log_entries.map(e => `
          <tr style="cursor:default">
            <td>${esc(e.entry_date)}</td>
            <td>${fmtHours(e.hours)}</td>
            <td>${e.location ? esc(e.location) : '—'}</td>
            <td>${esc(e.activity_description)}</td>
            <td>${statusBadge(e.status)}</td>
          </tr>`).join('');

    setHtml($('main-content'), `
      <button class="back-link" id="back-btn">← Nazaj na seznam</button>

      <div class="detail-header">
        <div class="detail-avatar">${initials}</div>
        <div>
          <div class="detail-name">${esc(v.first_name + ' ' + v.last_name)}</div>
          <div class="detail-meta">${esc(v.phone)}${v.email ? ' · ' + esc(v.email) : ''}</div>
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

      ${v.log_entries.length === 0 ? `
        <div style="margin:0 0 1.5rem">
          <button class="btn btn-danger btn-sm" id="delete-btn">Izbriši prostovoljca</button>
          <span style="font-size:0.8rem;color:var(--text-muted);margin-left:0.75rem">Samo prostovoljci brez vnosov se lahko izbrišejo.</span>
        </div>
      ` : ''}

      <p class="section-title">Dnevnik dela</p>
      <div class="table-wrapper">
        <table>
          <thead><tr>
            <th>Datum</th><th>Ure</th><th>Lokacija</th><th>Opis</th><th>Status</th>
          </tr></thead>
          <tbody>${entriesRows}</tbody>
        </table>
      </div>
    `);

    $('back-btn').addEventListener('click', () => {
      history.pushState(null, '', '#volunteers');
      renderList();
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
  return new Date(iso).toLocaleDateString('sl-SI', { year: 'numeric', month: 'long', day: 'numeric' });
}

// ===== Settings page =====
async function renderSettings() {
  $('topbar-title').textContent = 'Nastavitve';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="settings"]')?.classList.add('active');

  setHtml($('main-content'), `<div style="padding:2.5rem;text-align:center"><span class="spinner"></span></div>`);

  let manager;
  try {
    manager = await API.managers.me();
  } catch (err) {
    setHtml($('main-content'), `<p class="form-error" style="margin:2rem">Napaka: ${esc(err.message)}</p>`);
    return;
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
      <div id="s-ngo-error" class="form-error" style="display:none"></div>
      <div class="form-actions"><button class="btn btn-primary btn-sm" id="s-ngo-save">Shrani</button></div>
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
      ngo_name:        $('s-ngo-name').value.trim(),
      ngo_street:      $('s-ngo-street').value.trim(),
      ngo_postal_code: $('s-ngo-postal').value.trim(),
      ngo_city:        $('s-ngo-city').value.trim(),
    };
    if (Object.values(payload).some(v => !v)) {
      showErr('s-ngo-error', 'Vsa polja so obvezna.'); return;
    }
    if (!/^\d{4}$/.test(payload.ngo_postal_code)) {
      showErr('s-ngo-error', 'Poštna številka mora biti 4-mestna številka.'); return;
    }
    try {
      await API.managers.update(payload);
      toast('Podatki organizacije so bili shranjeni.');
    } catch (err) {
      showErr('s-ngo-error', err.message);
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
    ${approvalsSortTh('Datum', 'entry_date')}
    <th>Prostovoljec</th>
    ${approvalsSortTh('Opis dela', 'activity_description')}
    ${approvalsSortTh('Ure', 'hours')}
    ${approvalsSortTh('Lokacija', 'location')}
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
    setHtml(tbody, `<tr class="empty-row"><td colspan="7">${msg}</td></tr>`);
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
        <td>${esc(e.entry_date)}</td>
        <td data-stop><a href="#volunteers/${e.volunteer_id}" style="color:var(--accent);text-decoration:none">${esc(name)}</a></td>
        <td>${desc}</td>
        <td style="text-align:right">${fmtHours(e.hours)}</td>
        <td>${e.location ? esc(e.location) : '—'}</td>
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

async function renderApprovals() {
  $('topbar-title').textContent = 'Odobritve';
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
      <h1 class="page-title">Odobritve</h1>
    </div>

    <div class="filter-bar">
      <select id="a-status">
        ${statusOpt('pending_manager', 'Čaka odobritev')}
        ${statusOpt('approved',        'Odobreno')}
        ${statusOpt('rejected',        'Zavrnjeno')}
        ${statusOpt('',               'Vsi')}
      </select>
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
    approvalsState.filter.search_q = '';
    approvalsState.filter.date_from = null;
    approvalsState.filter.date_to   = null;
    $('a-search-q').value  = '';
    $('a-date-from').value = '';
    $('a-date-to').value   = '';
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

// ===== Log entry detail =====
async function renderLogEntryDetail(id) {
  revokePhotoUrls();
  $('topbar-title').textContent = 'Vnos';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="approvals"]')?.classList.add('active');
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
  const tileStyle  = 'position:relative;width:130px;height:130px;background:var(--border);border-radius:var(--radius);overflow:hidden;cursor:pointer;flex-shrink:0';
  const delStyle   = 'position:absolute;top:4px;right:4px;width:26px;height:26px;background:rgba(0,0,0,0.55);color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:18px;line-height:26px;text-align:center;padding:0';
  const phStyle    = 'width:130px;height:130px;background:var(--border);border-radius:var(--radius);opacity:0.35;flex-shrink:0';

  const photoTiles = entry.photos.length > 0
    ? entry.photos.map(p => `
        <div class="photo-tile" data-photo-id="${p.id}" style="${tileStyle}">
          <img data-photo-id="${p.id}" src="${BLANK}" alt="Fotografija"
               style="width:100%;height:100%;object-fit:cover;display:block" />
          ${editable ? `<button class="photo-del-btn" data-photo-id="${p.id}" style="${delStyle}" title="Izbriši">×</button>` : ''}
        </div>`).join('')
    : `<div data-placeholder style="${phStyle}"></div><div data-placeholder style="${phStyle}"></div>`;

  const addTile = editable ? `
    <label for="photo-upload"
           style="width:130px;height:130px;border:2px dashed var(--border);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text-muted);font-size:2.5rem;flex-shrink:0"
           title="Dodaj fotografijo">+</label>
    <input type="file" id="photo-upload" accept="image/*" multiple style="display:none" />` : '';

  setHtml($('main-content'), `
    <button class="back-link" id="back-btn">← Nazaj na odobritve</button>

    <div class="detail-header">
      <div>
        <div class="detail-name">${esc(entry.entry_date)}</div>
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
        <div class="info-label">Prostovoljec</div>
        <div class="info-value"><a href="#volunteers/${entry.volunteer_id}" style="color:var(--accent)">${esc(volName)}</a></div>
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
          <div class="photo-tile" data-photo-id="${photo.id}" style="${tileStyle}">
            <img data-photo-id="${photo.id}" src="${BLANK}" alt="Fotografija"
                 style="width:100%;height:100%;object-fit:cover;display:block" />
            <button class="photo-del-btn" data-photo-id="${photo.id}" style="${delStyle}" title="Izbriši">×</button>
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
    history.pushState(null, '', '#approvals');
    renderApprovals();
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
        history.pushState(null, '', '#approvals');
        renderApprovals();
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
      const desc  = $('d-desc').value.trim();
      const hours = parseFloat($('d-hours').value);
      const errEl = $('d-edit-error');
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
      errEl.hidden = true;
      $('d-save-btn').disabled = true;
      $('d-save-btn').textContent = 'Shranjevanje…';
      try {
        const updated = await API.logEntries.update(entry.id, { activity_description: desc, hours });
        entry = updated;
        $('d-desc-display').textContent = updated.activity_description;
        $('d-hours-display').textContent = fmtHours(updated.hours);
        toast('Vnos posodobljen.');
      } catch (err) {
        errEl.textContent = err.message;
        errEl.hidden = false;
      }
      $('d-save-btn').disabled = false;
      $('d-save-btn').textContent = 'Shrani spremembe';
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
