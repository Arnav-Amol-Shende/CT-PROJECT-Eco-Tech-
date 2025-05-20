document.querySelectorAll('a[href]').forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
  
      if (href && !href.startsWith('#')) {
        e.preventDefault(); 
        document.body.classList.add('fade-out'); 
  
        setTimeout(() => {
          window.location.href = href;
        }, 500);
      }
    });
  });

  window.addEventListener('load', () => {
    document.body.classList.remove('fade-out');
  });
  