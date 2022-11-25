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

function lTclicked(){
  if(ddabongLeftTop.style.display == 'none'){
      ddabongLeftTop.style.display = 'block'
      leftTopResized.style.filter = 'opacity(0.3)'
      selectedArray.push("resized_leftTop_"+localStorage.getItem("pic_name"));
  }
  else{
    ddabongLeftTop.style.display = 'none'
    leftTopResized.style.filter = 'opacity(1)'
    selectedArray.pop("resized_leftTop_"+localStorage.getItem("pic_name"));
  }
  console.log("----------------------");
  for (let value of selectedArray.values()) {
    console.log(value);
  }
  console.log("----------------------");
}

function mTclicked(){
  if(ddabongMidTop.style.display == 'none'){
      ddabongMidTop.style.display = 'block'
      midTopResized.style.filter = 'opacity(0.3)'
      selectedArray.push("resized_midTop_"+localStorage.getItem("pic_name"));
  }
  else{
    ddabongMidTop.style.display = 'none'
    midTopResized.style.filter = 'opacity(1)'
    selectedArray.pop("resized_midTop_"+localStorage.getItem("pic_name"));
  }
  console.log("----------------------");
  for (let value of selectedArray.values()) {
    console.log(value);
  }
  console.log("----------------------");
}

function rTclicked(){
  if(ddabongRightTop.style.display == 'none'){
      ddabongRightTop.style.display = 'block'
      rightTopResized.style.filter = 'opacity(0.3)'
      selectedArray.push("resized_rightTop_"+localStorage.getItem("pic_name"));
  }
  else{
    ddabongRightTop.style.display = 'none'
    rightTopResized.style.filter = 'opacity(1)'
    selectedArray.pop("resized_rightTop_"+localStorage.getItem("pic_name"));
  }
  console.log("----------------------");
  for (let value of selectedArray.values()) {
    console.log(value);
  }
  console.log("----------------------");
}
