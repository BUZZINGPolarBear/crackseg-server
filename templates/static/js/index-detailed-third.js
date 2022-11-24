window.onload = function(){
  //좌상단
  leftTopResized.src = "/templates/static/images/resized/resized_leftTop_"+ localStorage.getItem("pic_name")
  leftTopPredicted.src = "/templates/static/images/predicted/resized_leftTop_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //중상단
  midTopResized.src = "/templates/static/images/resized/resized_midTop_"+ localStorage.getItem("pic_name")
  midTopPredicted.src = "/templates/static/images/predicted/resized_midTop_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //우상단
  rightTopResized.src = "/templates/static/images/resized/resized_rightTop_"+ localStorage.getItem("pic_name")
  rightTopPredicted.src = "/templates/static/images/predicted/resized_rightTop_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"

  //----- 중간 -----
  //좌중단
  leftMidResized.src = "/templates/static/images/resized/resized_leftMid_"+ localStorage.getItem("pic_name")
  leftMidPredicted.src = "/templates/static/images/predicted/resized_leftMid_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //중중단
  midMidResized.src = "/templates/static/images/resized/resized_midMid_"+ localStorage.getItem("pic_name")
  midMidPredicted.src = "/templates/static/images/predicted/resized_midMid_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //우중단
  rightMidResized.src = "/templates/static/images/resized/resized_rightMid_"+ localStorage.getItem("pic_name")
  rightMidPredicted.src = "/templates/static/images/predicted/resized_rightMid_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"

  //----- 하단 -----
  //좌하단
  leftBotResized.src = "/templates/static/images/resized/resized_leftBot_"+ localStorage.getItem("pic_name")
  leftBotPredicted.src = "/templates/static/images/predicted/resized_leftBot_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //중하단
  midBotResized.src = "/templates/static/images/resized/resized_midBot_"+ localStorage.getItem("pic_name")
  midBotPredicted.src = "/templates/static/images/predicted/resized_midBot_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  //우하단
  rightBotResized.src = "/templates/static/images/resized/resized_rightBot_"+ localStorage.getItem("pic_name")
  rightBotPredicted.src = "/templates/static/images/predicted/resized_rightBot_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
}

var topSlider = document.getElementById("topImgSlider");
var topOutput = document.getElementById("topValue");
topOutput.innerHTML = topSlider.value; // Display the default slider value

var midSlider = document.getElementById("midImgSlider");
var midOutput = document.getElementById("midValue");
midOutput.innerHTML = midSlider.value; // Display the default slider value

var botSlider = document.getElementById("botImgSlider");
var botOutput = document.getElementById("botValue");
botOutput.innerHTML = botSlider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
topSlider.oninput = function() {
  topOutput.innerHTML = this.value;
  $('.topRow').css('opacity', (this.value/100));
}

midSlider.oninput = function() {
  midOutput.innerHTML = this.value;
  $('.midRow').css('opacity', (this.value/100));
}

botSlider.oninput = function() {
  botOutput.innerHTML = this.value;
  $('.botRow').css('opacity', (this.value/100));
}

