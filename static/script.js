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

  $('#email-pdf').click((e) => {
    e.preventDefault();
    $('#email-form-container').toggleClass('d-none');
  });

  $('#send-email').click(function(e) {
    e.preventDefault();
    let pdfPath = $('#pdf').attr('src').slice(1);
    let form = $(this).closest('form');
    let input = $('<input>')
                  .attr('type', 'hidden')
                  .attr('name', 'pdf')
                  .val(pdfPath)
    form.append(input);
    form.submit();
  });
});
