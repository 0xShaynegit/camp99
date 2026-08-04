// Camp 99 — vanilla JS, replaces jQuery/jQuery UI/Swiper

function initStickyHeader() {
  var header = document.querySelector('.site-header');
  if (!header) return;
  function update() {
    header.classList.toggle('is-scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
}

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

function initCarousel() {
  var track = document.querySelector('.carousel__track');
  if (!track) return;
  var prev = document.querySelector('.carousel__btn--prev');
  var next = document.querySelector('.carousel__btn--next');
  var scrollAmount = function () {
    var item = track.querySelector('.carousel__item');
    return item ? item.getBoundingClientRect().width + 12 : 300;
  };
  prev.addEventListener('click', function () {
    track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
  });
  next.addEventListener('click', function () {
    track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
  });
}

function initScrollToTop() {
  var btn = document.querySelector('.scroll-to-top');
  if (!btn) return;
  btn.hidden = false;

  function updateContrast() {
    var prevVisibility = btn.style.visibility;
    btn.style.visibility = 'hidden';
    var x = window.innerWidth - 24 - 22;
    var y = window.innerHeight - 24 - 22;
    var el = document.elementFromPoint(x, y);
    btn.style.visibility = prevVisibility;

    var bg = 'rgba(0, 0, 0, 0)';
    while (el) {
      var c = getComputedStyle(el).backgroundColor;
      if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') { bg = c; break; }
      el = el.parentElement;
    }
    var m = bg.match(/\d+(\.\d+)?/g);
    if (m && m.length >= 3) {
      var luminance = (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]);
      btn.classList.toggle('scroll-to-top--on-light', luminance > 150);
    }
  }

  window.addEventListener('scroll', function () {
    btn.classList.toggle('is-visible', window.scrollY > 400);
    updateContrast();
  }, { passive: true });
  window.addEventListener('resize', updateContrast, { passive: true });
  updateContrast();

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initStickyHeader();
  initNav();
  initCarousel();
  initScrollToTop();
});
