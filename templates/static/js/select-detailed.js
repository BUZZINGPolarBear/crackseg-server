var selectedArray = new Array()

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

function submitBtn(){
  if(leftTop.style.display == 'block') selectedArray.push("resized_leftTop_"+localStorage.getItem("pic_name"));
  if(midTop.style.display == 'block') selectedArray.push("resized_midTop_"+localStorage.getItem("pic_name"));
  if(rightTop.style.display == 'block') selectedArray.push("resized_rightTop_"+localStorage.getItem("pic_name"));

  if(leftMid.style.display == 'block') selectedArray.push("resized_leftMid_"+localStorage.getItem("pic_name"));
  if(midMid.style.display == 'block') selectedArray.push("resized_midMid_"+localStorage.getItem("pic_name"));
  if(rightMid.style.display == 'block') selectedArray.push("resized_rightMid_"+localStorage.getItem("pic_name"));

  if(leftBot.style.display == 'block') selectedArray.push("resized_leftBot_"+localStorage.getItem("pic_name"));
  if(midBot.style.display == 'block') selectedArray.push("resized_midBot_"+localStorage.getItem("pic_name"));
  if(rightBot.style.display == 'block') selectedArray.push("resized_rightBot_"+localStorage.getItem("pic_name"));

  console.log(selectedArray)
}