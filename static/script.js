$(document).ready(function () {
  $('#print-pdf').click((e) => {
    e.preventDefault();
    console.log('printing');
  })

  $('#download-pdf').click((e) => {
    e.preventDefault();
    console.log('downloading');
  });
});
