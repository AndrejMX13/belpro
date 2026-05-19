'use strict';

// ===== Reports page =====

const SL_MONTHS = [
  '', 'Januar', 'Februar', 'Marec', 'April', 'Maj', 'Junij',
  'Julij', 'Avgust', 'September', 'Oktober', 'November', 'December',
];

const reportsState = {
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1,
  withEntriesOnly: false,
};

async function renderReports() {
  $('topbar-title').textContent = 'Poročila';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="reports"]')?.classList.add('active');

  const currentYear = new Date().getFullYear();
  const yearOptions = [];
  for (let y = currentYear + 1; y >= 2024; y--) {
    yearOptions.push(`<option value="${y}"${y === reportsState.year ? ' selected' : ''}>${y}</option>`);
  }
  const monthOptions = SL_MONTHS.slice(1).map((name, i) => {
    const m = i + 1;
    return `<option value="${m}"${m === reportsState.month ? ' selected' : ''}>${name}</option>`;
  }).join('');

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Poročila</h1>
      <div style="display:flex;gap:0.5rem;align-items:center">
        <button class="btn btn-secondary" id="send-reports-btn">Pošlji poročila</button>
        <button class="btn btn-primary" id="export-all-btn">Izvozi vse (PDF)</button>
      </div>
    </div>
    <div id="send-reports-result"></div>
    <div class="filter-bar">
      <label for="r-year">Leto:</label>
      <select id="r-year">${yearOptions.join('')}</select>
      <label for="r-month">Mesec:</label>
      <select id="r-month">${monthOptions}</select>
      <label class="checkbox-label">
        <input type="checkbox" id="r-entries-only"${reportsState.withEntriesOnly ? ' checked' : ''} />
        Samo z vnosi v mesecu
      </label>
    </div>
    <div id="reports-content">
      <div class="loading-row"><span class="spinner"></span></div>
    </div>
    <div style="margin-top:2rem">
      <button id="toggle-archive-btn" class="btn btn-ghost"
              style="width:100%;text-align:left;padding:0.5rem 0;font-weight:600;border:none;border-bottom:1px solid var(--border);border-radius:0;cursor:pointer">
        &#9660; Arhiv poro&#269;il
      </button>
      <div id="reports-archive" hidden>
        <div class="loading-row"><span class="spinner"></span></div>
      </div>
    </div>
  `);

  $('r-year').addEventListener('change', () => {
    reportsState.year = parseInt($('r-year').value, 10);
    loadReports();
  });
  $('r-month').addEventListener('change', () => {
    reportsState.month = parseInt($('r-month').value, 10);
    loadReports();
  });
  $('r-entries-only').addEventListener('change', () => {
    reportsState.withEntriesOnly = $('r-entries-only').checked;
    loadReports();
  });
  $('export-all-btn').addEventListener('click', () => exportReportPdf(null));
  $('send-reports-btn').addEventListener('click', sendReports);

  await loadReports();

  let archiveLoaded = false;
  $('toggle-archive-btn').addEventListener('click', () => {
    const container = $('reports-archive');
    const btn = $('toggle-archive-btn');
    if (!container) return;
    const isHidden = container.hasAttribute('hidden');
    if (isHidden) {
      container.removeAttribute('hidden');
      btn.textContent = '▲ Arhiv poročil';
      if (!archiveLoaded) {
        archiveLoaded = true;
        loadReportArchive();
      }
    } else {
      container.setAttribute('hidden', '');
      btn.textContent = '▼ Arhiv poročil';
    }
  });
}

async function loadReports() {
  const content = $('reports-content');
  if (!content) return;
  setHtml(content, '<div class="loading-row"><span class="spinner"></span></div>');
  try {
    const data = await API.reports.monthly(reportsState.year, reportsState.month, reportsState.withEntriesOnly);
    renderReportsTable(data);
  } catch (err) {
    setHtml(content, `<p class="error-text">Napaka pri nalaganju: ${esc(err.message)}</p>`);
  }
}

function renderReportsTable(data) {
  const content = $('reports-content');
  if (!content) return;

  if (data.items.length === 0) {
    setHtml(content, '<p class="empty-state">Ni prostovoljcev ali odobrenih vnosov za izbrano obdobje.</p>');
    return;
  }

  const monthLabel = `${SL_MONTHS[data.month]} ${data.year}`;

  const rows = data.items.map(item => `
    <tr data-id="${item.volunteer_id}">
      <td>${esc(item.last_name)} ${esc(item.first_name)}</td>
      <td class="num-cell">${fmtHours(item.total_hours)}</td>
      <td class="num-cell">${item.entry_count}</td>
      <td class="td-actions" data-stop>
        <button class="btn btn-ghost btn-sm export-vol-btn"
                data-vol-id="${item.volunteer_id}"
                ${item.entry_count === 0 ? 'disabled' : ''}>
          Izvozi PDF
        </button>
      </td>
    </tr>
  `).join('');

  setHtml(content, `
    <p class="reports-period">
      Obdobje: <strong>${monthLabel}</strong> &mdash;
      skupaj <strong>${fmtHours(data.total_hours)} ur</strong>,
      <strong>${data.total_entries}</strong> odobrenih vnosov
    </p>
    <div class="table-wrapper">
      <table id="reports-table">
        <thead><tr>
          <th>Prostovoljec</th>
          <th class="num-cell">Ure</th>
          <th class="num-cell">Vnosi</th>
          <th></th>
        </tr></thead>
        <tbody>${rows}</tbody>
        <tfoot><tr class="totals-row">
          <td><strong>Skupaj</strong></td>
          <td class="num-cell"><strong>${fmtHours(data.total_hours)}</strong></td>
          <td class="num-cell"><strong>${data.total_entries}</strong></td>
          <td></td>
        </tr></tfoot>
      </table>
    </div>
  `);

  content.querySelectorAll('tr[data-id]').forEach(row => {
    row.addEventListener('click', (e) => {
      if (e.target.closest('[data-stop]')) return;
      location.hash = '#reports/volunteer/' + row.dataset.id;
    });
  });

  content.querySelectorAll('.export-vol-btn').forEach(btn => {
    btn.addEventListener('click', () => exportReportPdf(btn.dataset.volId));
  });
}

async function exportReportPdf(volunteerId) {
  try {
    const { blob, filename } = await API.reports.exportPdf(reportsState.year, reportsState.month, volunteerId);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err) {
    toast('Napaka pri izvozu: ' + err.message, 'error');
  }
}

async function sendReports() {
  const btn = $('send-reports-btn');
  const resultEl = $('send-reports-result');
  if (!btn) return;

  btn.disabled = true;
  btn.textContent = 'Pošiljam…';
  if (resultEl) setHtml(resultEl, '');

  try {
    const r = await API.reports.sendMonthly(reportsState.year, reportsState.month);

    const lines = [];
    if (r.sent_via_email.length)
      lines.push(`E-pošta (${r.sent_via_email.length}): ${r.sent_via_email.map(esc).join(', ')}`);
    if (r.sent_via_whatsapp.length)
      lines.push(`WhatsApp (${r.sent_via_whatsapp.length}): ${r.sent_via_whatsapp.map(esc).join(', ')}`);
    if (r.skipped_no_entries.length)
      lines.push(`Brez vnosov: ${r.skipped_no_entries.map(esc).join(', ')}`);
    if (r.skipped_no_channel.length)
      lines.push(`Brez kanala: ${r.skipped_no_channel.map(esc).join(', ')}`);
    const mgr = [];
    if (r.manager_email_sent) mgr.push('e-pošta');
    if (r.manager_whatsapp_sent) mgr.push('WhatsApp');
    lines.push(`Upravljalec: ${mgr.length ? mgr.join(' + ') : 'preskočeno'}`);
    if (r.errors.length)
      lines.push(`Napake: ${r.errors.map(esc).join('; ')}`);

    const hasErrors = r.errors.length > 0;
    if (resultEl) {
      setHtml(resultEl, `
        <div style="margin:0.75rem 0;padding:0.75rem 1rem;border-radius:6px;font-size:0.85rem;line-height:1.6;
                    background:${hasErrors ? 'var(--warning-bg,#fff8e1)' : 'var(--success-bg,#e8f5e9)'};
                    border:1px solid ${hasErrors ? 'var(--warning-border,#ffe082)' : 'var(--success-border,#a5d6a7)'}">
          ${lines.map(l => `<div>${l}</div>`).join('')}
        </div>
      `);
    }
  } catch (err) {
    toast('Napaka pri pošiljanju: ' + esc(err.message), 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Pošlji poročila';
  }
}

function fmtHours(h) {
  return Number(h).toFixed(1);
}

async function loadReportArchive() {
  const container = $('reports-archive');
  if (!container) return;

  try {
    const data = await API.reports.history();

    if (data.items.length === 0) {
      setHtml(container, '<p class="empty-state" style="padding:0.75rem 0">Ni shranjenih poročil.</p>');
      return;
    }

    const rows = data.items.map(item => {
      const period = `${SL_MONTHS[item.period_month]} ${item.period_year}`;
      const name = item.volunteer_name || 'Skupno';
      const sentAt = item.sent_at
        ? new Date(item.sent_at).toLocaleDateString('sl-SI')
        : '—';
      return `
        <tr>
          <td>${esc(period)}</td>
          <td>${esc(name)}</td>
          <td>${esc(sentAt)}</td>
          <td class="td-actions" data-stop>
            <button class="btn btn-ghost btn-sm" data-archive-id="${esc(item.id)}">Prenesi</button>
          </td>
        </tr>
      `;
    }).join('');

    setHtml(container, `
      <div class="table-wrapper" style="margin-top:0.75rem">
        <table>
          <thead><tr>
            <th>Obdobje</th>
            <th>Prostovoljec</th>
            <th>Poslano</th>
            <th></th>
          </tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `);

    container.querySelectorAll('[data-archive-id]').forEach(btn => {
      btn.addEventListener('click', () => downloadHistoryPdf(btn.dataset.archiveId));
    });
  } catch (err) {
    setHtml(container, `<p class="error-text" style="padding:0.75rem 0">Napaka pri nalaganju arhiva: ${esc(err.message)}</p>`);
  }
}

async function downloadHistoryPdf(reportId) {
  try {
    const { blob, filename } = await API.reports.downloadHistoryPdf(reportId);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err) {
    toast('Napaka pri prenosu: ' + esc(err.message), 'error');
  }
}
