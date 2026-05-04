'use strict';

const analyticsState = {
  year:  new Date().getFullYear(),
  month: new Date().getMonth() + 1,
  _data: null,
};

let _chartVol   = null;
let _chartLoc   = null;
let _chartTrend = null;

async function renderAnalytics() {
  $('topbar-title').textContent = 'Analitika';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="analytics"]')?.classList.add('active');

  const currentYear = new Date().getFullYear();
  const yearOptions = [];
  for (let y = currentYear + 1; y >= 2024; y--) {
    yearOptions.push(`<option value="${y}"${y === analyticsState.year ? ' selected' : ''}>${y}</option>`);
  }
  const monthOptions = SL_MONTHS.slice(1).map((name, i) => {
    const m = i + 1;
    return `<option value="${m}"${m === analyticsState.month ? ' selected' : ''}>${name}</option>`;
  }).join('');

  setHtml($('main-content'), `
    <div class="page-header">
      <h1 class="page-title">Analitika</h1>
      <button class="btn btn-ghost btn-sm" id="an-csv-btn">Izvozi CSV</button>
    </div>
    <div class="filter-bar">
      <label for="an-year">Leto:</label>
      <select id="an-year">${yearOptions.join('')}</select>
      <label for="an-month">Mesec:</label>
      <select id="an-month">${monthOptions}</select>
    </div>
    <div id="analytics-content">
      <div class="loading-row"><span class="spinner"></span></div>
    </div>
  `);

  $('an-year').addEventListener('change', () => {
    analyticsState.year = parseInt($('an-year').value, 10);
    loadAnalytics();
  });
  $('an-month').addEventListener('change', () => {
    analyticsState.month = parseInt($('an-month').value, 10);
    loadAnalytics();
  });
  $('an-csv-btn').addEventListener('click', exportAnalyticsCsv);

  await loadAnalytics();
}

async function loadAnalytics() {
  const content = $('analytics-content');
  if (!content) return;
  setHtml(content, '<div class="loading-row"><span class="spinner"></span></div>');
  _destroyCharts();
  try {
    const data = await API.analytics.summary(analyticsState.year, analyticsState.month);
    analyticsState._data = data;
    renderAnalyticsContent(content, data);
  } catch (err) {
    setHtml(content, `<p class="error-text">Napaka pri nalaganju: ${esc(err.message)}</p>`);
  }
}

function renderAnalyticsContent(container, data) {
  const noActivity = data.active_volunteer_count - data.hours_per_volunteer.length;
  const monthLabel = SL_MONTHS[data.month] + ' ' + data.year;
  const volHeight  = Math.max(200, data.hours_per_volunteer.length * 36);

  container.innerHTML = `
    <div class="kpi-grid">
      <div class="kpi-tile">
        <div class="kpi-value">${fmtHours(data.total_hours)}</div>
        <div class="kpi-label">Ure v mesecu</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-value">${data.active_volunteer_count}</div>
        <div class="kpi-label">Aktivni prostovoljci</div>
      </div>
      <div class="kpi-tile kpi-warning">
        <div class="kpi-value">${data.entries_pending}</div>
        <div class="kpi-label">Čaka odobritev</div>
      </div>
      <div class="kpi-tile kpi-success">
        <div class="kpi-value">${data.entries_approved}</div>
        <div class="kpi-label">Odobreno</div>
      </div>
      <div class="kpi-tile kpi-danger">
        <div class="kpi-value">${data.entries_rejected}</div>
        <div class="kpi-label">Zavrnjeno</div>
      </div>
      <div class="kpi-tile kpi-neutral">
        <div class="kpi-value">${noActivity}</div>
        <div class="kpi-label">Brez vnosov ta mesec</div>
      </div>
    </div>

    <div class="chart-grid">
      <div class="chart-card">
        <div class="chart-title">Ure po prostovoljcih — ${monthLabel}</div>
        ${data.hours_per_volunteer.length > 0
          ? `<div class="chart-canvas-wrap" style="height:${volHeight}px"><canvas id="chart-vol"></canvas></div>`
          : '<p class="empty-state">Ni odobrenih ur za izbrano obdobje.</p>'}
      </div>
      <div class="chart-card">
        <div class="chart-title">Ure po lokacijah — ${monthLabel}</div>
        ${data.hours_per_location.length > 0
          ? '<div class="chart-canvas-wrap"><canvas id="chart-loc"></canvas></div>'
          : '<p class="empty-state">Ni odobrenih ur za izbrano obdobje.</p>'}
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-title">Mesečni trend — zadnjih 6 mesecev</div>
      <div class="chart-canvas-wrap chart-canvas-wrap-trend"><canvas id="chart-trend"></canvas></div>
    </div>
  `;

  _renderCharts(data);
}

function _renderCharts(data) {
  const primary = '#1a5276';
  const accent  = '#2e86c1';

  if (data.hours_per_volunteer.length > 0) {
    _chartVol = new Chart($('chart-vol'), {
      type: 'bar',
      data: {
        labels: data.hours_per_volunteer.map(v => v.full_name),
        datasets: [{ data: data.hours_per_volunteer.map(v => Number(v.total_hours)), backgroundColor: primary }],
      },
      options: {
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, ticks: { font: { size: 11 } } },
          y: { grid: { display: false }, ticks: { font: { size: 11 } } },
        },
      },
    });
  }

  if (data.hours_per_location.length > 0) {
    _chartLoc = new Chart($('chart-loc'), {
      type: 'bar',
      data: {
        labels: data.hours_per_location.map(l => l.location),
        datasets: [{ data: data.hours_per_location.map(l => Number(l.total_hours)), backgroundColor: accent }],
      },
      options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 11 }, maxRotation: 30 } },
          y: { beginAtZero: true, ticks: { font: { size: 11 } } },
        },
      },
    });
  }

  const trendLabels = data.monthly_trend.map(p => SL_MONTHS[p.month].slice(0, 3) + ' ' + String(p.year).slice(2));
  _chartTrend = new Chart($('chart-trend'), {
    type: 'line',
    data: {
      labels: trendLabels,
      datasets: [{
        data: data.monthly_trend.map(p => Number(p.total_hours)),
        borderColor: primary,
        backgroundColor: 'rgba(26,82,118,.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointBackgroundColor: primary,
      }],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11 } } },
        y: { beginAtZero: true, ticks: { font: { size: 11 } } },
      },
    },
  });
}

function _destroyCharts() {
  if (_chartVol)   { _chartVol.destroy();   _chartVol   = null; }
  if (_chartLoc)   { _chartLoc.destroy();   _chartLoc   = null; }
  if (_chartTrend) { _chartTrend.destroy(); _chartTrend = null; }
}

function exportAnalyticsCsv() {
  const d = analyticsState._data;
  if (!d) return;

  const rows = [
    ['Ime in priimek', 'Ure (odobrene)'],
    ...d.hours_per_volunteer.map(v => [v.full_name, v.total_hours]),
    [],
    ['Lokacija', 'Ure (odobrene)'],
    ...d.hours_per_location.map(l => [l.location, l.total_hours]),
    [],
    ['Mesec', 'Skupaj ur'],
    ...d.monthly_trend.map(p => [SL_MONTHS[p.month] + ' ' + p.year, p.total_hours]),
  ];

  const csv = rows
    .map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(','))
    .join('\n');
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `analitika_${d.year}_${String(d.month).padStart(2, '0')}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}
