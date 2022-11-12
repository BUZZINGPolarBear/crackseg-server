// window.onload = function(){
//   const location = "/templates/static/images/predicted/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
//   const resized_img_location = "/templates/static/images/resized/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpeg"
//   predicted_img.src = location
//   resized_img.src = resized_img_location
// }

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

