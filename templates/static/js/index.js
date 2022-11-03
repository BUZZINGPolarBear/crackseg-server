imgInp.onchange = evt => {
  const [file] = imgInp.files
  if (file) {
    crack_img.src = URL.createObjectURL(file)
  }
}

$("#imgInp").on('change',function(){
  var fileName = $("#imgInp").val();
  $(".upload-name").val(fileName);
});