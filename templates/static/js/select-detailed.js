

var selectedArray = new Array()
var notSelectedArray = new Array()

window.onload = function(){
  //----- 상부 -----
  //좌상단
  leftTopResized.src = "/templates/static/images/resized/resized_leftTop_"+ localStorage.getItem("pic_name")
  //중상단
  midTopResized.src = "/templates/static/images/resized/resized_midTop_"+ localStorage.getItem("pic_name")
  //우상단
  rightTopResized.src = "/templates/static/images/resized/resized_rightTop_"+ localStorage.getItem("pic_name")

  //----- 중간 -----
  //좌중단
  leftMidResized.src = "/templates/static/images/resized/resized_leftMid_"+ localStorage.getItem("pic_name")
  //중중단
  midMidResized.src = "/templates/static/images/resized/resized_midMid_"+ localStorage.getItem("pic_name")
  //우중단
  rightMidResized.src = "/templates/static/images/resized/resized_rightMid_"+ localStorage.getItem("pic_name")

  //----- 하단 -----
  //좌하단
  leftBotResized.src = "/templates/static/images/resized/resized_leftBot_"+ localStorage.getItem("pic_name")
  //중하단
  midBotResized.src = "/templates/static/images/resized/resized_midBot_"+ localStorage.getItem("pic_name")
  //우하단
  rightBotResized.src = "/templates/static/images/resized/resized_rightBot_"+ localStorage.getItem("pic_name")
}

function selectItems(selectedId){
  const nowSelected = document.getElementById(selectedId)
  const img_id = document.getElementById( selectedId+"Resized")

  if(nowSelected.style.display == 'none'){
      nowSelected.style.display = 'block'
      img_id.style.filter = 'opacity(0.3)'
  }
  else{
    nowSelected.style.display = 'none'
    img_id.style.filter = 'opacity(1)'
  }
}

async function submitBtn(){
  if(leftTop.style.display == 'none') notSelectedArray.push("resized_leftTop_"+localStorage.getItem("pic_name"));
  if(midTop.style.display == 'none') notSelectedArray.push("resized_midTop_"+localStorage.getItem("pic_name"));
  if(rightTop.style.display == 'none') notSelectedArray.push("resized_rightTop_"+localStorage.getItem("pic_name"));

  if(leftMid.style.display == 'none') notSelectedArray.push("resized_leftMid_"+localStorage.getItem("pic_name"));
  if(midMid.style.display == 'none') notSelectedArray.push("resized_midMid_"+localStorage.getItem("pic_name"));
  if(rightMid.style.display == 'none') notSelectedArray.push("resized_rightMid_"+localStorage.getItem("pic_name"));

  if(leftBot.style.display == 'none') notSelectedArray.push("resized_leftBot_"+localStorage.getItem("pic_name"));
  if(midBot.style.display == 'none') notSelectedArray.push("resized_midBot_"+localStorage.getItem("pic_name"));
  if(rightBot.style.display == 'none') notSelectedArray.push("resized_rightBot_"+localStorage.getItem("pic_name"));

  //--------------------

  if(leftTop.style.display == 'block') selectedArray.push("resized_leftTop_"+localStorage.getItem("pic_name"));
  if(midTop.style.display == 'block') selectedArray.push("resized_midTop_"+localStorage.getItem("pic_name"));
  if(rightTop.style.display == 'block') selectedArray.push("resized_rightTop_"+localStorage.getItem("pic_name"));

  if(leftMid.style.display == 'block') selectedArray.push("resized_leftMid_"+localStorage.getItem("pic_name"));
  if(midMid.style.display == 'block') selectedArray.push("resized_midMid_"+localStorage.getItem("pic_name"));
  if(rightMid.style.display == 'block') selectedArray.push("resized_rightMid_"+localStorage.getItem("pic_name"));

  if(leftBot.style.display == 'block') selectedArray.push("resized_leftBot_"+localStorage.getItem("pic_name"));
  if(midBot.style.display == 'block') selectedArray.push("resized_midBot_"+localStorage.getItem("pic_name"));
  if(rightBot.style.display == 'block') selectedArray.push("resized_rightBot_"+localStorage.getItem("pic_name"));

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "selectedPicArray": notSelectedArray
  });
  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };
  localStorage.setItem("selectedArea", JSON.stringify(selectedArray));
  await postAPI(hostAddr+"crack-seg/remove-imgs/detailed", requestOptions)
  location.href = "/loading/detailed"
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