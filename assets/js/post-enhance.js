document.addEventListener('DOMContentLoaded', function() {
  var callouts = document.querySelectorAll('.callout');
  callouts.forEach(function(callout) {
    var title = callout.querySelector('p');
    if (!title) return;

    var header = document.createElement('div');
    header.className = 'callout-header';

    var toggle = document.createElement('span');
    toggle.className = 'callout-toggle';
    toggle.textContent = "\u25be";

    var titleSpan = document.createElement('span');
    titleSpan.className = 'callout-title-text';
    titleSpan.innerHTML = title.innerHTML;

    header.appendChild(toggle);
    header.appendChild(titleSpan);

    var body = document.createElement('div');
    body.className = 'callout-body';

    var nodes = [];
    var next = title.nextElementSibling;
    while (next) {
      nodes.push(next);
      next = next.nextElementSibling;
    }
    nodes.forEach(function(n) { body.appendChild(n); });

    callout.insertBefore(header, title);
    callout.insertBefore(body, title.nextSibling);
    callout.removeChild(title);

    callout.classList.add('collapsible');

    // Use addEventListener for toggle
    header.addEventListener('click', function() {
      var b = this.nextElementSibling;
      var ic = this.querySelector('.callout-toggle');
      if (b.classList.contains('collapsed')) {
        b.classList.remove('collapsed');
        ic.textContent = "\u25be";
      } else {
        b.classList.add('collapsed');
        ic.textContent = "\u25b8";
      }
    });
  });
});
