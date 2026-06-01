/** Sticky Navbar **/
let mainHeader = document.querySelector('#main-header')
if (mainHeader) {
  const stickyNav = () => {
    if (window.scrollY > 50) {
        mainHeader.classList.add('shadow-sm');
    } else {
        mainHeader.classList.remove('shadow-sm');
    }
  }
  window.addEventListener('load', stickyNav)
  document.addEventListener('scroll', stickyNav)
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
