document.addEventListener('DOMContentLoaded', function() {
  var content = document.querySelector('.blog-post');
  var tocContainer = document.getElementById('toc-content');
  if (!content || !tocContainer) return;

  var headings = content.querySelectorAll('h2, h3');
  if (headings.length < 2) {
    document.getElementById('toc-sidebar').style.display = 'none';
    return;
  }

  var toc = document.createElement('ul');
  toc.className = 'toc-list';

  var headingItems = [];

  headings.forEach(function(h) {
    if (!h.id) {
      h.id = h.textContent.toLowerCase().replace(/[^\w\u4e00-\u9fff]+/g, '-').replace(/^-|-$/g, '');
    }

    var li = document.createElement('li');
    li.className = (h.tagName === 'H3') ? 'toc-h3' : 'toc-h2';

    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;

    a.addEventListener('click', function(e) {
      e.preventDefault();
      var top = h.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: top, behavior: 'smooth' });
      history.pushState(null, null, '#' + h.id);
    });

    li.appendChild(a);
    toc.appendChild(li);
    headingItems.push({ el: h, link: li });
  });

  tocContainer.appendChild(toc);

  // IntersectionObserver for active tracking
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          headingItems.forEach(function(item) {
            item.link.classList.remove('active');
            if (item.el.id === entry.target.id) {
              item.link.classList.add('active');
            }
          });
        }
      });
    }, { rootMargin: '-80px 0px -65% 0px' });

    headingItems.forEach(function(item) {
      observer.observe(item.el);
    });
  }
});
