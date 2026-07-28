document.addEventListener('DOMContentLoaded', function() {
  var callouts = document.querySelectorAll('.callout');
  callouts.forEach(function(callout) {
    var title = callout.querySelector('p');
    if (!title) return;

    var header = document.createElement('div');
    header.className = 'callout-header';
    header.setAttribute('onclick', 'toggleCallout(this)');

    var toggle = document.createElement('span');
    toggle.className = 'callout-toggle';
    toggle.textContent = '\u25be';

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

    // Move nodes into body (removes from original position)
    nodes.forEach(function(n) { body.appendChild(n); });

    callout.insertBefore(header, title);
    callout.insertBefore(body, title.nextSibling);
    callout.removeChild(title);

    callout.classList.add('collapsible');
  });
});

function toggleCallout(header) {
  var body = header.nextElementSibling;
  var icon = header.querySelector('.callout-toggle');
  if (body.classList.contains('collapsed')) {
    body.classList.remove('collapsed');
    icon.textContent = '\u25be';
  } else {
    body.classList.add('collapsed');
    icon.textContent = '\u25b8';
  }
}
