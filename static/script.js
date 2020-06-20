$(document).ready(function () {
  $('#print-pdf').click((e) => {
    e.preventDefault();

    let pdf = $('#pdf')[0];
    pdf.focus();
    pdf.contentWindow.print();
  });

  $('#download-pdf').click((e) => {
    e.preventDefault();
    window.location = e.target.href;
  });
});
