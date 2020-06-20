// document.addEventListener('DOMContentLoaded', loadscreen);


//alert("connected");
function loadscreen(){
   var str = '<div class="jumbotron text-center"><h1 class="display-4">Please wait</h1><hr class="my-4"><p class="lead mb-0">Your video transcription will be ready soon.</p></div><div class="d-flex justify-content-center"><div class="spinner-border p-4 mt-5" style="width: 5rem; height: 5rem; role="status"><span class="sr-only">Processing...</span></div></div>'
   var replace = document.getElementById('upload_form');
   var p_replace = replace.parentNode;
   p_replace.removeChild(replace);
   p_replace.innerHTML = str + p_replace.innerHTML;
}

// Update the current slider value (each time you drag the slider handle)
function updateTextInput(val) {
          document.getElementById('slider_label').textContent=val;
}
