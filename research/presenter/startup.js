/* Small ES5 bootstrap: visible diagnostics even if a later script cannot parse.
   This never reads or changes a simulation state, coupling or readout. */
(function (root) {
  'use strict';
  var panel = document.getElementById('startup');
  var title = document.getElementById('startup-title');
  var status = document.getElementById('startup-status');
  var finished = false;
  var blocked = false;
  function fail(message) {
    if (finished) return;
    blocked = true;
    panel.hidden = false;
    panel.setAttribute('data-phase', 'failed');
    title.textContent = 'The interactive viewer could not start';
    status.textContent = String(message);
    var loading = document.getElementById('loading');
    if (loading) loading.hidden = true;
  }
  root.PresenterStartup = {
    failed: fail,
    isBlocked: function () { return blocked; },
    complete: function () {
      finished = true;
      blocked = false;
      panel.setAttribute('data-phase', 'ready');
      panel.hidden = true;
    }
  };
  root.addEventListener('error', function (event) {
    var source = event.target && event.target.getAttribute && event.target.getAttribute('src');
    fail(source ? 'A required viewer script could not load: ' + source :
      'A viewer script failed before startup completed. ' + (event.message || 'Open this file in a current browser.'));
  }, true);
  root.addEventListener('unhandledrejection', function (event) {
    var reason = event.reason;
    fail('Startup stopped: ' + (reason && reason.message ? reason.message : String(reason)));
  });
  panel.setAttribute('data-phase', 'checking');
  status.textContent = 'JavaScript is running. Checking this browser before opening the recorded experiments…';
  var missing = [];
  if (typeof root.BigInt !== 'function') missing.push('BigInt');
  if (typeof root.Promise !== 'function') missing.push('Promises');
  if (typeof root.TextEncoder !== 'function') missing.push('TextEncoder');
  if (!root.crypto || !root.crypto.subtle || typeof root.crypto.subtle.digest !== 'function') missing.push('Web Crypto SHA-256');
  try {
    if (!document.createElement('canvas').getContext('2d')) missing.push('Canvas 2D');
  } catch (error) { missing.push('Canvas 2D'); }
  if (missing.length) fail('This browser view is missing: ' + missing.join(', ') + '. Open the HTML in a current browser. Web Crypto may require HTTPS or localhost.');
  root.addEventListener('load', function () {
    if (!finished && !blocked && !root.PresenterUI) {
      fail('The viewer did not initialize. A required script may be unavailable or unsupported. The embedded recording list remains available here.');
    }
  });
})(window);
