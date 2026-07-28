document.addEventListener('DOMContentLoaded', function() {
  var callouts = document.querySelectorAll('.callout');
  callouts.forEach(function(callout) {
    var title = callout.querySelector('p');
    if (!title) return;

    var details = document.createElement('details');
    details.className = callout.className;
    var st = callout.style.cssText;
    st = st.replace(/padding[^;]+;/g, '').replace(/border-radius[^;]+;/g, '');
    details.style.cssText = st;

    var summary = document.createElement('summary');
    summary.className = 'callout-summary';
    summary.innerHTML = title.innerHTML;

    var nodes = [];
    var next = title.nextElementSibling;
    while (next) {
      nodes.push(next);
      next = next.nextElementSibling;
    }

    details.appendChild(summary);
    nodes.forEach(function(n) { details.appendChild(n); });

    callout.parentNode.replaceChild(details, callout);
  });
});
