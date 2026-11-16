/* Mądry Portfel — przycisk „Udostępnij” i „Kopiuj link” pod artykułami. Bez skryptów zewnętrznych. */
(function () {
  function init() {
    document.querySelectorAll('.share').forEach(function (box) {
      var url = box.getAttribute('data-url') || location.href;
      var title = box.getAttribute('data-title') || document.title;
      var native = box.querySelector('[data-share-native]');
      var copy = box.querySelector('[data-share-copy]');
      var note = box.querySelector('.share-note');
      if (native && navigator.share) {
        native.hidden = false;
        native.addEventListener('click', function () {
          navigator.share({ title: title, url: url }).catch(function () {});
        });
      }
      if (copy) {
        copy.addEventListener('click', function () {
          var done = function () { if (note) { note.textContent = 'Link skopiowany.'; } };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(done, function () { window.prompt('Skopiuj link:', url); });
          } else {
            window.prompt('Skopiuj link:', url);
          }
        });
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
