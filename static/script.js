$(document).ready(function () {
  $('#print-pdf').click((e) => {
    e.preventDefault();

    let pdf = $('#pdf')[0];
    pdf.focus();
    pdf.contentWindow.print();
    console.log('printing');
  });

  $('#download-pdf').click((e) => {
    e.preventDefault();
    console.log('downloading');
  });
});
