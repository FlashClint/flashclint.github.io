document.addEventListener('DOMContentLoaded', function() {
  // Make callouts collapsible
  var callouts = document.querySelectorAll('.callout');
  callouts.forEach(function(callout) {
    var title = callout.querySelector('p');
    if (!title) return;

    // Create header
    var header = document.createElement('div');
    header.className = 'callout-header';
    header.setAttribute('onclick', 'toggleCallout(this)');

    var toggle = document.createElement('span');
    toggle.className = 'callout-toggle';
    toggle.textContent = '\u25be';  // ▾

    var titleSpan = document.createElement('span');
    titleSpan.className = 'callout-title-text';
    titleSpan.innerHTML = title.innerHTML;

    header.appendChild(toggle);
    header.appendChild(titleSpan);

    // Create body with remaining content
    var body = document.createElement('div');
    body.className = 'callout-body';

    var next = title.nextElementSibling;
    var nodes = [];
    while (next) {
      nodes.push(next);
      next = next.nextElementSibling;
    }
    nodes.forEach(function(n) { body.appendChild(n.cloneNode(true)); });

    // Replace title with header
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
