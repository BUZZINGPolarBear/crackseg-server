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
  localStorage.setItem("pic_name", fileName.split("\\")[2].replace(' ', '_'))
});

function toLoadingPage(){
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
    toLoadingPage()
    await postAPI("http://localhost:8000/crack-seg/fileupload/", requestOptions)
    location.href = "result/"
  }

}


async function postPic(host, options){
  fetch(host, options)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
}

//post API AS JSON
async function postAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  console.log(res)
}

function toLoadingPage(){
  html = `
        <div class="status-info" >
          <div style="text-align: center">1</div>사진 업로드 </div>
          <div>..........</div>
          <div class="status-info" id="now-status"><div style="text-align: center">2</div>균열 검출</div>
          <div>..........</div>
        <div class="status-info"><div style="text-align: center">3</div>결과 확인</div>
  `
  $('.status-area').empty()
  $('.status-area').append(html)

  html  = `
         <img class="crack_img" src="/templates/static/images/loading.gif" style="z-index: 9999" />
  `
  $('.file-upload-area').empty()
  $('.file-upload-area').css("height", "30vh")
  $('.file-upload-area').append(html)

  $('#loading_status').append('균열검출중...')
}