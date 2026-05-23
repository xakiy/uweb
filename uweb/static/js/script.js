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

/** Back to top button **/
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

// /** Sticky Navbar **/
// let mainHeader = document.querySelector('#main-header')
// if (mainHeader) {
//   const stickyNav = () => {
//     if (window.scrollY > 100) {
//         mainHeader.style.position='fixed';
//         mainHeader.style.top='0px';
//         mainHeader.classList.add('shadow-sm');
//         // mainHeader.classList.add('fixed-top');
//     } else {
//         mainHeader.style.position='initial';
//         mainHeader.style.top='-150px';
//         mainHeader.classList.remove('shadow-sm');
//         // mainHeader.classList.remove('fixed-top');
//     }
//   }
//   window.addEventListener('load', stickyNav)
//   document.addEventListener('scroll', stickyNav)
// }