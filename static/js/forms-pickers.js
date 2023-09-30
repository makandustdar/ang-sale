/**
 * Form Picker
 */

'use strict';

(function () {
  // Flat Picker
  // --------------------------------------------------------------------
  const flatpickrDateTime1 = document.querySelector('#flatpickr-datetime1')
  const flatpickrDateTime2 = document.querySelector('#flatpickr-datetime2')

  // Datetime
  if (flatpickrDateTime1) {
    flatpickrDateTime1.flatpickr({
      locale: 'fa',
      altInput: true,
      altFormat: 'Y/m/d',
      disableMobile: true
    });
  }
  if (flatpickrDateTime2) {
    flatpickrDateTime2.flatpickr({
      locale: 'fa',
      altInput: true,
      altFormat: 'Y/m/d',
      disableMobile: true
    });
  }
})();
