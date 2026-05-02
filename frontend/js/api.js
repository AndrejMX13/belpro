'use strict';

const API = (() => {
  const BASE = '/api';
  let _creds = null;

  function setPassword(password) {
    _creds = btoa('manager:' + password);
    sessionStorage.setItem('bpCreds', _creds);
  }

  function loadFromSession() {
    _creds = sessionStorage.getItem('bpCreds');
    return _creds !== null;
  }

  function clear() {
    _creds = null;
    sessionStorage.removeItem('bpCreds');
  }

  async function request(path, opts = {}) {
    const headers = { 'Content-Type': 'application/json' };
    if (_creds) headers['Authorization'] = 'Basic ' + _creds;
    Object.assign(headers, opts.headers || {});

    const res = await fetch(BASE + path, { ...opts, headers });

    if (res.status === 401) {
      clear();
      window.dispatchEvent(new CustomEvent('belpro:unauthorized'));
      const err = new Error('Seja je potekla. Prijavite se znova.');
      err.status = 401;
      throw err;
    }

    if (res.status === 204) return null;

    if (!res.ok) {
      let detail = 'HTTP ' + res.status;
      try { detail = (await res.json()).detail || detail; } catch { /* empty */ }
      const err = new Error(detail);
      err.status = res.status;
      throw err;
    }

    return res.json();
  }

  return {
    setPassword,
    loadFromSession,
    clear,

    health: () => request('/health'),

    managers: {
      me:    ()     => request('/managers/me'),
      setup: (data) => request('/managers', { method: 'POST', body: JSON.stringify(data) }),
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
      deactivate: (id)   => request('/volunteers/' + id + '/deactivate', { method: 'PATCH' }),
      delete:     (id)   => request('/volunteers/' + id, { method: 'DELETE' }),
    },
  };
})();
