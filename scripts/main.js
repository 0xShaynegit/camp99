// Camp 99 — vanilla JS, replaces jQuery/jQuery UI/Swiper

function initNav() {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });

  var items = document.querySelectorAll('.has-children');
  items.forEach(function (item) {
    var closeTimer = null;
    var isDesktop = function () { return window.innerWidth > 1024; };

    function open() {
      clearTimeout(closeTimer);
      item.classList.add('is-open');
      var btn = item.querySelector(':scope > .submenu-toggle');
      if (btn) btn.setAttribute('aria-expanded', 'true');
    }
    function scheduleClose() {
      closeTimer = setTimeout(function () {
        item.classList.remove('is-open');
        var btn = item.querySelector(':scope > .submenu-toggle');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }, 250);
    }

    item.addEventListener('mouseenter', function () { if (isDesktop()) open(); });
    item.addEventListener('mouseleave', function () { if (isDesktop()) scheduleClose(); });

    var btn = item.querySelector(':scope > .submenu-toggle');
    if (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (item.classList.contains('is-open')) {
          item.classList.remove('is-open');
          btn.setAttribute('aria-expanded', 'false');
        } else {
          open();
        }
      });
    }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-nav')) {
      document.querySelectorAll('.has-children.is-open').forEach(function (el) {
        el.classList.remove('is-open');
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initNav();
  // carousel and scroll-to-top modules attach themselves here
  // (added in Tasks 5 and 7)
});
