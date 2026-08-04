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
  window.addEventListener('scroll', function () {
    btn.classList.toggle('is-visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initNav();
  initCarousel();
  initScrollToTop();
});
