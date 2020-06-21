var payload = {filepath:null};
var dataLoop = null;

//Continue to ping the server until it indicates the transcription has completed
function fetchdata(){
  payload.filepath = $('#filepath').val() || '';

  $.ajax({
   url: '/processStatus',
   type: 'post',
   data: JSON.stringify(payload),
   success: function(response){
     if (response.complete){
        clearTimeout(dataLoop);
        process_complete();
      }else{
        dataLoop = setTimeout(fetchdata,7000);
      }
   },
 });
}

//Once this happens, make a post request to load the editTranscription page
function process_complete(){
    payload.filepath = document.getElementById("filepath").value;

    $.ajax({
     url: '/processComplete',
     type: 'post',
     data: JSON.stringify(payload),
     success: function(response){
        $('body').html(response)
     }
   });
}

document.addEventListener('DOMContentLoaded', () => {
  dataLoop = setTimeout(fetchdata,7000);
});
