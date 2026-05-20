'use strict';

// ===== Administracija page =====

async function renderAdmin() {
  $('topbar-title').textContent = 'Administracija';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="admin"]')?.classList.add('active');

  const card = 'background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin-bottom:1.5rem';
  const h2   = 'font-size:1rem;font-weight:600;margin:0 0 1.25rem';

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Administracija</h1>
    </div>
    ${healthWidgetHTML()}
    <div style="${card}">
      <h2 style="${h2}">Sistemske nastavitve</h2>
      <div id="admin-settings-loading" style="padding:1rem;text-align:center">
        <span class="spinner"></span>
      </div>
      <div id="admin-settings-form" hidden>
        <div class="field">
          <label for="a-max-photos">Najve&#269;je &#353;tevilo fotografij na vnos</label>
          <input id="a-max-photos" type="number" min="1" style="width:100%;max-width:12rem" step="1" />
        </div>
        <div class="field">
          <label for="a-photo-retention">Hranjenje fotografij (dni)</label>
          <input id="a-photo-retention" type="number" min="1" style="width:100%;max-width:12rem" step="1" />
        </div>
        <div class="field">
          <label for="a-session-duration">Trajanje seje (ure)</label>
          <input id="a-session-duration" type="number" min="1" style="width:100%;max-width:12rem" step="1" />
        </div>
        <div id="admin-settings-error" class="form-error" style="display:none"></div>
        <div class="form-actions">
          <button class="btn btn-primary btn-sm" id="a-save-btn">Shrani</button>
        </div>
      </div>
      <div id="admin-settings-load-error" class="form-error" style="display:none"></div>
    </div>
  `);

  // Load current settings
  let original = {};
  try {
    const data = await API.admin.getSettings();
    original = { ...data };

    $('a-max-photos').value      = data.max_photos_per_entry;
    $('a-photo-retention').value = data.photo_retention_days;
    $('a-session-duration').value = data.session_duration_hours;

    $('admin-settings-loading').hidden = true;
    $('admin-settings-form').hidden    = false;
  } catch (err) {
    $('admin-settings-loading').hidden = true;
    const errEl = $('admin-settings-load-error');
    errEl.textContent = 'Napaka pri nalaganju nastavitev: ' + esc(err.message);
    errEl.style.display = 'block';
    return;
  }

  // Save handler
  $('a-save-btn').addEventListener('click', async () => {
    const errEl = $('admin-settings-error');
    errEl.style.display = 'none';

    const current = {
      max_photos_per_entry:  parseInt($('a-max-photos').value, 10),
      photo_retention_days:  parseInt($('a-photo-retention').value, 10),
      session_duration_hours: parseInt($('a-session-duration').value, 10),
    };

    // Validate
    for (const [key, val] of Object.entries(current)) {
      if (!Number.isInteger(val) || val < 1) {
        errEl.textContent = 'Vse vrednosti morajo biti cela števila, večja ali enaka 1.';
        errEl.style.display = 'block';
        return;
      }
    }

    // Collect only changed fields
    const patch = {};
    for (const [key, val] of Object.entries(current)) {
      if (val !== original[key]) patch[key] = val;
    }

    if (Object.keys(patch).length === 0) {
      toast('Ni sprememb za shraniti.', 'info');
      return;
    }

    const btn = $('a-save-btn');
    btn.disabled = true;
    btn.textContent = 'Shranjujem…';

    try {
      await API.admin.updateSettings(patch);
      original = { ...current };
      toast('Nastavitve so bile shranjene.');
    } catch (err) {
      errEl.textContent = 'Napaka pri shranjevanju: ' + esc(err.message);
      errEl.style.display = 'block';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Shrani';
    }
  });

  startHealthWidget();
}
