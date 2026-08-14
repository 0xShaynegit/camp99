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
  var handleScroll = function (direction) {
    var maxScroll = track.scrollWidth - track.clientWidth;
    var newScroll = track.scrollLeft + (direction === 'next' ? scrollAmount() : -scrollAmount());
    if (newScroll <= 0) {
      track.scrollLeft = maxScroll;
    } else if (newScroll >= maxScroll) {
      track.scrollLeft = 0;
    } else {
      track.scrollBy({ left: direction === 'next' ? scrollAmount() : -scrollAmount(), behavior: 'smooth' });
    }
  };
  prev.addEventListener('click', function () {
    handleScroll('prev');
  });
  next.addEventListener('click', function () {
    handleScroll('next');
  });
}

function initLightbox() {
  var lightboxHTML = '<div class="lightbox" hidden><div class="lightbox__overlay"></div><div class="lightbox__container"><button class="lightbox__close" aria-label="Close">✕</button><img class="lightbox__img" src="" alt=""><div class="lightbox__nav"><button class="lightbox__prev" aria-label="Previous">❮</button><button class="lightbox__next" aria-label="Next">❯</button></div></div></div>';
  document.body.insertAdjacentHTML('beforeend', lightboxHTML);
  var lightbox = document.querySelector('.lightbox');
  var img = lightbox.querySelector('.lightbox__img');
  var closeBtn = lightbox.querySelector('.lightbox__close');
  var prevBtn = lightbox.querySelector('.lightbox__prev');
  var nextBtn = lightbox.querySelector('.lightbox__next');
  var overlay = lightbox.querySelector('.lightbox__overlay');
  var allCarouselItems = [];
  var currentIndex = 0;
  function openLightbox(index) {
    currentIndex = index;
    img.src = allCarouselItems[index].src;
    img.alt = allCarouselItems[index].alt;
    lightbox.hidden = false;
  }
  function closeLightbox() {
    lightbox.hidden = true;
  }
  function navigateLightbox(direction) {
    currentIndex = direction === 'next' ? (currentIndex + 1) % allCarouselItems.length : (currentIndex - 1 + allCarouselItems.length) % allCarouselItems.length;
    openLightbox(currentIndex);
  }
  var carouselItems = document.querySelectorAll('.carousel__item');
  carouselItems.forEach(function (item, i) {
    allCarouselItems.push(item);
    item.style.cursor = 'pointer';
    item.addEventListener('click', function () { openLightbox(i); });
  });
  closeBtn.addEventListener('click', closeLightbox);
  overlay.addEventListener('click', closeLightbox);
  prevBtn.addEventListener('click', function () { navigateLightbox('prev'); });
  nextBtn.addEventListener('click', function () { navigateLightbox('next'); });
  document.addEventListener('keydown', function (e) {
    if (!lightbox.hidden) {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') navigateLightbox('prev');
      if (e.key === 'ArrowRight') navigateLightbox('next');
    }
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
  initLightbox();
  initScrollToTop();
});
