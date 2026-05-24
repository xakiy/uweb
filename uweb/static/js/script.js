/**
 * Header fixed top on scroll
 */
let selectHeader = document.querySelector('#main-header');
if (selectHeader) {
  let breadcrumbDiv = document.querySelector('#main-breadcrumb')
  const scrollHeight = breadcrumbDiv.offsetTop
  const headerFixed = () => {
    if (window.scrollY > scrollHeight) {
      selectHeader.classList.add('fixed-top', 'shadow-sm');
      breadcrumbDiv.style.paddingTop=scrollHeight+"px";
    } else {
      selectHeader.classList.remove('fixed-top', 'shadow-sm')
      breadcrumbDiv.style.paddingTop=0;
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