'use strict';

const API = (() => {
  const BASE = '/api';

  function _authHeaders(extra = {}) {
    return { ...extra };
  }

  function _handleUnauthorized() {
    window.dispatchEvent(new CustomEvent('belpro:unauthorized'));
    const err = new Error('Seja je potekla. Prijavite se znova.');
    err.status = 401;
    return err;
  }

  async function request(path, opts = {}) {
    const headers = _authHeaders({ 'Content-Type': 'application/json' });
    Object.assign(headers, opts.headers || {});

    const res = await fetch(BASE + path, { ...opts, headers });

    if (res.status === 401) throw _handleUnauthorized();
    if (res.status === 204) return null;

    if (!res.ok) {
      let detail = 'HTTP ' + res.status;
      try {
        const body = await res.json();
        if (Array.isArray(body.detail)) {
          detail = body.detail.map(e => String(e.msg).replace(/^Value error,\s*/i, '')).join('; ');
        } else {
          detail = body.detail || detail;
        }
      } catch { /* empty */ }
      const err = new Error(detail);
      err.status = res.status;
      throw err;
    }

    return res.json();
  }

  async function downloadRequest(path, opts = {}) {
    const headers = _authHeaders();
    Object.assign(headers, opts.headers || {});

    const res = await fetch(BASE + path, { ...opts, headers });

    if (res.status === 401) throw _handleUnauthorized();

    if (!res.ok) {
      let detail = 'HTTP ' + res.status;
      try {
        const body = await res.json();
        if (Array.isArray(body.detail)) {
          detail = body.detail.map(e => String(e.msg).replace(/^Value error,\s*/i, '')).join('; ');
        } else {
          detail = body.detail || detail;
        }
      } catch { /* empty */ }
      const err = new Error(detail);
      err.status = res.status;
      throw err;
    }

    const blob = await res.blob();
    const disposition = res.headers.get('Content-Disposition') || '';
    const match = disposition.match(/filename="?([^"]+)"?/);
    const filename = match ? match[1] : 'porocilo.pdf';
    return { blob, filename };
  }

  return {
    auth: {
      login:  (password) => request('/auth/login',  { method: 'POST', body: JSON.stringify({ password }) }),
      logout: ()         => request('/auth/logout', { method: 'POST' }),
    },

    health: () => request('/health'),

    managers: {
      me:             ()     => request('/managers/me'),
      setup:          (data) => request('/managers',                    { method: 'POST',  body: JSON.stringify(data) }),
      update:         (data) => request('/managers/me',                 { method: 'PATCH', body: JSON.stringify(data) }),
      changePassword: (data) => request('/managers/me/change-password', { method: 'POST',  body: JSON.stringify(data) }),
      configInfo:     ()     => request('/managers/me/config-info'),
    },

    volunteers: {
      list:       (params = {}) => {
        const q = new URLSearchParams();
        for (const [k, v] of Object.entries(params)) {
          if (v !== null && v !== undefined && v !== '') q.set(k, String(v));
        }
        return request('/volunteers?' + q);
      },
      checkEmso:  (emso) => request('/volunteers/check-emso', { method: 'POST', body: JSON.stringify({ emso }) }),
      create:     (data) => request('/volunteers', { method: 'POST', body: JSON.stringify(data) }),
      get:        (id)   => request('/volunteers/' + id),
      activate:   (id)   => request('/volunteers/' + id + '/activate',   { method: 'PATCH' }),
      deactivate: (id)   => request('/volunteers/' + id + '/deactivate', { method: 'PATCH' }),
      update:     (id, data) => request('/volunteers/' + id, { method: 'PATCH', body: JSON.stringify(data) }),
      delete:     (id)   => request('/volunteers/' + id, { method: 'DELETE' }),
    },

    logEntries: {
      get:    (id)       => request('/log-entries/' + id),
      create: (payload)  => request('/log-entries', { method: 'POST', body: JSON.stringify(payload) }),
      update: (id, data) => request('/log-entries/' + id, { method: 'PATCH', body: JSON.stringify(data) }),

      uploadPhoto: (entryId, formData) => {
        return fetch(BASE + '/log-entries/' + entryId + '/photos', {
          method: 'POST', body: formData,
        }).then(async res => {
          if (res.status === 401) {
            window.dispatchEvent(new CustomEvent('belpro:unauthorized'));
            const err = new Error('Seja je potekla. Prijavite se znova.');
            err.status = 401;
            throw err;
          }
          if (!res.ok) {
            let detail = 'HTTP ' + res.status;
            try { detail = (await res.json()).detail || detail; } catch { /* empty */ }
            const err = new Error(detail);
            err.status = res.status;
            throw err;
          }
          return res.json();
        });
      },

      photoUrl: async (entryId, photoId) => {
        const res = await fetch(
          BASE + '/log-entries/' + entryId + '/photos/' + photoId + '/file'
        );
        if (!res.ok) return null;
        return URL.createObjectURL(await res.blob());
      },

      deletePhoto: (entryId, photoId) =>
        request('/log-entries/' + entryId + '/photos/' + photoId, { method: 'DELETE' }),
      list: (params = {}) => {
        const q = new URLSearchParams();
        for (const [k, v] of Object.entries(params)) {
          if (v !== null && v !== undefined && v !== '') q.set(k, String(v));
        }
        return request('/log-entries?' + q);
      },
      approve: (id) => request('/log-entries/' + id + '/approve', { method: 'PATCH' }),
      reject:  (id) => request('/log-entries/' + id + '/reject',  { method: 'PATCH' }),
      deleteEntry: (id) => request('/log-entries/' + id, { method: 'DELETE' }),
    },

    analytics: {
      summary: (year, month) => {
        const q = new URLSearchParams({ year, month });
        return request('/analytics/summary?' + q);
      },
    },

    reports: {
      monthly: (year, month, withEntriesOnly = false) =>
        request(`/reports/monthly?year=${year}&month=${month}&with_entries_only=${withEntriesOnly}`),
      exportPdf: (year, month, volunteerId = null) => {
        const q = new URLSearchParams({ year, month });
        if (volunteerId) q.set('volunteer_id', volunteerId);
        return downloadRequest('/reports/monthly/pdf?' + q, { method: 'POST' });
      },
      sendMonthly: (year, month) =>
        request(`/reports/send-monthly?year=${year}&month=${month}`, { method: 'POST' }),
    },
  };
})();
