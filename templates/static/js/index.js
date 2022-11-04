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

crackImgSubmitBtn.onclick = async function(){
  if(fileName.length==0){
    alert("사진 파일을 입력해주세요.")
  }
  else{
    var formdata = new FormData();
    const file = imgInp.files[0]
    formdata.append("title", "Test");
    formdata.append("imgfile", file, fileName);

    var requestOptions = {
      method: 'POST',
      body: formdata,
      redirect: 'follow'
    };

    await postPic("http://localhost:8000/crack-seg/fileupload/", requestOptions)
  }

}


async function postPic(host, options){
  fetch(host, options)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
}
