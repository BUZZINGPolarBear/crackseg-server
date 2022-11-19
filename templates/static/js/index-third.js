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
showCrackInfo()

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
  $('#predicted_img').css('opacity', (this.value/100));
}

//분석된 균열 정보 보여주기
async function showCrackInfo(){
  var raw = JSON.stringify({
  "img_name": localStorage.getItem("pic_name")
  });

  var requestOptions = {
    method: 'POST',
    body: raw,
    redirect: 'follow'
  };
  const crack_info = await postAPI(hostAddr+"crack-seg/vision-inference/info/", requestOptions)
  console.log(crack_info)
}

//post API AS JSON
async function postAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  return data
}