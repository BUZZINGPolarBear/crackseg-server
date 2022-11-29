var selectedArray = new Array()
var crackvisionJson = new Array()

window.onload = async function(){
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

  const selectedBoxJson = JSON.parse(localStorage.getItem("selectedArea"))
  for(key in selectedBoxJson){
    var raw = JSON.stringify({
      "img_name": selectedBoxJson[key].split('resized_')[1],
      "length": localStorage.getItem("length")
    });

    var requestOptions = {
      method: 'POST',
      body: raw,
      redirect: 'follow'
    };
    const crack_info = await postAPI(hostAddr+"crack-seg/vision-inference/info/", requestOptions)
    var data = new Object();
    idTemp = selectedBoxJson[key].split('resized_')[1]
    idTemp = idTemp.split('_')[0]
    data.img_name = idTemp;
    data.all_crack_length = crack_info.all_crack_length
    data.average_crack_width = crack_info.average_crack_width
    data.real_max_width = crack_info.real_max_width

    crackvisionJson.push(data)
  }
  console.log(crackvisionJson)
}

function selectItems(selectedId){
  const nowSelected = document.getElementById(selectedId)
  const img_id = document.getElementById( selectedId+"Resized")

  if(UrlExists("/templates/static/images/predicted/resized_"+selectedId+"_"+localStorage.getItem("pic_name")) == 0) return
  if(nowSelected.style.display == 'none'){
      nowSelected.style.display = 'block'
      img_id.src = "/templates/static/images/predicted/resized_"+selectedId+"_"+localStorage.getItem("pic_name")
  }
  else{
    nowSelected.style.display = 'none'
    img_id.src = "/templates/static/images/resized/resized_"+selectedId+"_"+localStorage.getItem("pic_name")
  }
}

async function submitBtn(){
  if(leftTop.style.display == 'none') selectedArray.push("resized_leftTop_"+localStorage.getItem("pic_name"));
  if(midTop.style.display == 'none') selectedArray.push("resized_midTop_"+localStorage.getItem("pic_name"));
  if(rightTop.style.display == 'none') selectedArray.push("resized_rightTop_"+localStorage.getItem("pic_name"));

  if(leftMid.style.display == 'none') selectedArray.push("resized_leftMid_"+localStorage.getItem("pic_name"));
  if(midMid.style.display == 'none') selectedArray.push("resized_midMid_"+localStorage.getItem("pic_name"));
  if(rightMid.style.display == 'none') selectedArray.push("resized_rightMid_"+localStorage.getItem("pic_name"));

  if(leftBot.style.display == 'none') selectedArray.push("resized_leftBot_"+localStorage.getItem("pic_name"));
  if(midBot.style.display == 'none') selectedArray.push("resized_midBot_"+localStorage.getItem("pic_name"));
  if(rightBot.style.display == 'none') selectedArray.push("resized_rightBot_"+localStorage.getItem("pic_name"));

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "selectedPicArray": selectedArray
  });
  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };
  await postAPI(hostAddr+"crack-seg/remove-imgs/detailed", requestOptions)
  location.href = "/loading/detailed"
}

//post API AS JSON
async function postAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  return data
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

function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}