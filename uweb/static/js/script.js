/**
 * Header fixed top on scroll
 */
let selectHeader = document.querySelector('#header');
if (selectHeader) {
  let headerOffset = selectHeader.offsetTop
  let nextElement = selectHeader.nextElementSibling
  const headerFixed = () => {
    if ((headerOffset - window.scrollY) <= 0) {
      selectHeader.classList.add('fixed-top')
      nextElement.classList.add('scrolled-offset')
    } else {
      selectHeader.classList.remove('fixed-top')
      nextElement.classList.remove('scrolled-offset')
    }
  }
  window.addEventListener('load', headerFixed)
  document.addEventListener('scroll', headerFixed)
}

/**
 * Back to top button
 */
let backtotop = document.querySelector('.back-to-top')
if (backtotop) {
  const toggleBacktotop = () => {
    if (window.scrollY > 100) {
      backtotop.classList.add('active')
    } else {
      backtotop.classList.remove('active')
    }
  }
  window.addEventListener('load', toggleBacktotop)
  document.addEventListener('scroll', toggleBacktotop)
}

/**
 * Splider
 */
var spliderCheck = document.getElementsByClassName("splide").length;
if (spliderCheck) {
  let splider = new Splide( '.splide', {
    type   : 'loop',
    drag   : 'free',
    focus  : 'center',
    perPage: 3,
    autoScroll: {
      speed: .5,
    },
  } );
  splider.mount( window.splide.Extensions );
}

/**
 * Animation on scroll
 */
window.addEventListener('load', () => {
  AOS.init({
    duration: 1000,
    easing: 'ease-in-out',
    once: true,
    mirror: false
  })
});
