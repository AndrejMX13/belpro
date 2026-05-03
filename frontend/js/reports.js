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
      <button class="btn btn-primary" id="export-all-btn">Izvozi vse (PDF)</button>
    </div>
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

  await loadReports();
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

function fmtHours(h) {
  return Number(h).toFixed(1);
}
