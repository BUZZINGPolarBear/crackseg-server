const crackImgSubmitBtn = document.getElementById("crack-img-submit-btn")
var fileName = $("#imgInp").val();

imgInp.onchange = evt => {
  const [file] = imgInp.files
  if (file) {
    crack_img.src = URL.createObjectURL(file)
    localStorage.setItem("pic_url", toString(crack_img.src))
  }
}

$("#imgInp").on('change',function(){
  fileName = $("#imgInp").val();
  $(".upload-name").val(fileName);
  localStorage.setItem("pic_name", fileName)
});

function toLoadingPage(){
  console.log("hi")
  location.href="loading/"
}

crackImgSubmitBtn.onclick = function(){
  if(fileName.length==0){
    alert("사진 파일을 입력해주세요.")
  }
  else{
    location.href="loading/"
  }

}