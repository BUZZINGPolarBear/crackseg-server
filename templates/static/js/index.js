const crackImgModalBtn = document.getElementById("crack-img-submit-btn");
const detailedImgModalBtn = document.getElementById("detailed-crack-img-submit-btn");
var fileName = $("#imgInp").val();
var length = 2;


imgInp.onchange = evt => {
  const [file] = imgInp.files
  if (file) {
    crack_img.src = URL.createObjectURL(file)
    localStorage.setItem("pic_url", toString(crack_img.src))
  }
}

$("#imgInp").on('change',function(){
  fileName = $("#imgInp").val();
  localStorage.setItem("original_img_name", fileName.split('\\')[2])
  $(".upload-name").val(fileName);
});

function toLoadingPage(){
  location.href="loading/"
}

const lengthSelectChange = (target) => {
        length = target.value;
        console.log(length)
}

//modals
crackImgModalBtn.onclick = function(){
    $('#modal-btn-area').empty()
    $('#modal-btn-area').append(`
    <button class="button is-primary modal-btn" id="normal-crack-btn">균열 측정하기</button>
    `)
    modal.style.display = "flex";

    const crackImgSubmitBtn = document.getElementById("normal-crack-btn");
    crackImgSubmitBtn.onclick = async function(){
    if(fileName.length==0){
    alert("사진 파일을 입력해주세요.")
    }
    else{
        var file_upload_formdata = new FormData(), remove_photo_formdata = new FormData();
        const file = imgInp.files[0];
        const pic_rand_id = makeid(15);

        modal.style.display = "none"
        toLoadingPage()
        localStorage.setItem("pic_name", pic_rand_id+`_${length}`+'.jpg')
        localStorage.setItem("length", length)

        remove_photo_formdata.append("img_name", localStorage.getItem("pic_name"))
        remove_photo_formdata.append("original_file_name", localStorage.getItem("original_img_name"))
        await postAPI(hostAddr + "crack-seg/remove-imgs")

        file_upload_formdata.append("title", pic_rand_id);
        file_upload_formdata.append("imgfile", file, fileName);
        file_upload_formdata.append("length", length);
        var requestOptions = {
        method: 'POST',
        body: file_upload_formdata,
        redirect: 'follow'
        };
        await postAPI(hostAddr+"crack-seg/fileupload/", requestOptions)

        $('#loading_status').empty();
        $('#loading_status').append('검출된 균열 분석중...')
        await getAPI(hostAddr + "crack-seg/vision-inference")
        location.href = "result/"
        }
    }
}

detailedImgModalBtn.onclick = function(){
  $('#modal-btn-area').empty()
  $('#modal-btn-area').append(`
   <button class="button is-warning modal-btn" id="detailed-crack-btn">균열 이미지 검출 부위 고르기</button>
  `)
   modal.style.display = "flex";

  const detailedCrackImgSubmitBtn = document.getElementById("detailed-crack-btn")
  detailedCrackImgSubmitBtn.onclick = async function(){
  if(fileName.length==0){
    alert("사진 파일을 입력해주세요.")
  }
  else{
      var formdata = new FormData();
      const file = imgInp.files[0];
      const pic_rand_id = makeid(15);

      formdata.append("title", pic_rand_id);
      formdata.append("imgfile", file, fileName);
      formdata.append("length", length);

      var requestOptions = {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
      };
      modal.style.display = "none"
      // toLoadingPage()
      localStorage.setItem("pic_name", pic_rand_id+`_${length}`+'.jpg')
      await getAPI(hostAddr + "crack-seg/remove-imgs")
      row_col_info = await postAPI(hostAddr+"crack-seg/fileuplaod/detailed", requestOptions)
      location.href = "/select/detailed"
    }
  }
}
const closeBtn = modal.querySelector(".close-area")
closeBtn.addEventListener("click", e => {
    modal.style.display = "none"
})

function toLoadingPage(){
    $('.button-area').empty()
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

//post API AS JSON
async function postAPI(host, options) {
    const res = await fetch(host, options)
    const data = res.json();
    return data
}

//get API
async function getAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  console.log(res)
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}