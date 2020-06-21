var payload = {filepath:null};
var loop
var loop2

//Continue to ping the server until it indicates the transcription has completed
function fetchdata(){
  payload.filepath = document.getElementById("filepath").value
  $.ajax({
   url: '/processStatus',
   type: 'post',
   data: JSON.stringify( payload ),
   success: function(response){
        console.log(response);
       if (response.complete == 'YES'){
          process_complete();
        }
        //alert(response);
   },
   complete:function(data){
   loop2 = setTimeout(fetchdata,10000);
  }
 });
}

document.addEventListener('DOMContentLoaded', function(){loop = setTimeout(fetchdata,10000);})

// $(document).ready(function(){
//  setTimeout(fetchdata,4000);
// });

//Once this happens, make a post request to load the editTranscription page
function process_complete(){
    clearTimeout(loop);
    clearTimeout(loop2);
    payload.filepath = document.getElementById("filepath").value
    $.ajax({
     url: '/processComplete',
     type: 'post',
     data: JSON.stringify( payload ),
     success: function(response){
          console.log(response);
           $('body').html(request.response)
          //alert(response);
     }
   });
}
