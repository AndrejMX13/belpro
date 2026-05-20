'use strict';

async function renderDocuments() {
  $('topbar-title').textContent = 'Dokumenti';
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelector('[data-page="documents"]')?.classList.add('active');

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
      <h1 class="page-title">Dokumenti</h1>
    </div>

    <div style="${card}">
      <h2 style="${h2}">Soglasje za obdelavo osebnih podatkov (GDPR)</h2>
      <p style="margin-bottom:1.25rem;color:var(--text-secondary,#6b7280);font-size:0.9rem">
        Prenesite obrazec, ki ga natisnete in izročite prostovoljcu v podpis pred začetkom sodelovanja.
        Obrazec je predizpolnjen s podatki vaše organizacije.
      </p>
      <div class="field">
        <label for="gdpr-clauses">Dodatne določbe <span style="font-weight:400;color:var(--text-secondary,#6b7280)">(neobvezno)</span></label>
        <textarea id="gdpr-clauses" rows="5" style="width:100%;box-sizing:border-box"
          placeholder="Sem vpišite morebitne dodatne določbe, ki bodo dodane na konec dokumenta. Polje pustite prazno, če dodatnih določb ni.">${esc(manager.gdpr_additional_clauses || '')}</textarea>
        <div class="form-hint">Besedilo bo dodano na konec dokumenta pod naslovom &ldquo;Dodatne določbe&rdquo;.</div>
      </div>
      <div id="gdpr-status" style="min-height:1.2rem;font-size:0.85rem;margin-bottom:0.5rem"></div>
      <div class="form-actions">
        <button class="btn btn-primary btn-sm" id="gdpr-download-btn">Prenesi PDF</button>
      </div>
    </div>
  `);

  const clausesEl = document.getElementById('gdpr-clauses');
  const statusEl  = document.getElementById('gdpr-status');
  const downloadBtn = document.getElementById('gdpr-download-btn');

  clausesEl.addEventListener('blur', async () => {
    statusEl.style.color = '';
    statusEl.textContent = 'Shranjevanje…';
    try {
      await API.managers.update({ gdpr_additional_clauses: clausesEl.value.trim() });
      statusEl.style.color = 'var(--success,#16a34a)';
      statusEl.textContent = 'Shranjeno.';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
    } catch (err) {
      statusEl.style.color = 'var(--danger,#dc2626)';
      statusEl.textContent = 'Napaka pri shranjevanju: ' + esc(err.message);
    }
  });

  downloadBtn.addEventListener('click', async () => {
    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Priprava…';
    try {
      const { blob, filename } = await API.documents.consentPdf();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      toast('Napaka pri generiranju PDF: ' + esc(err.message));
    } finally {
      downloadBtn.disabled = false;
      downloadBtn.textContent = 'Prenesi PDF';
    }
  });
}
