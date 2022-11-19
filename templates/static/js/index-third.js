var reader = new FileReader();

window.onload = function(){
  const location = "/templates/static/images/predicted/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  const resized_img_location = "/templates/static/images/resized/resized_"+ localStorage.getItem("pic_name")
  predicted_img.src = location
  resized_img.src = resized_img_location
}

var slider = document.getElementById("myRange");
var output = document.getElementById("value");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
  $('#predicted_img').css('opacity', (this.value/100));
}