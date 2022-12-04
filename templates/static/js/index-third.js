var reader = new FileReader();

window.onload = function(){
  const location = "/templates/static/images/predicted/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  const resized_img_location = "/templates/static/images/resized/resized_"+ localStorage.getItem("pic_name")
  const colored_crack_img = `
  /templates/static/images/analyzed/analyzed_${localStorage.getItem("pic_name")}
  `
  console.log(colored_crack_img)
  predicted_img.src = location
  resized_img.src = resized_img_location
  colored_img.src = colored_crack_img
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
  "img_name": localStorage.getItem("pic_name"),
  "length": localStorage.getItem("length")
  });

  var requestOptions = {
    method: 'POST',
    body: raw,
    redirect: 'follow'
  };
  const crack_info = await postAPI(hostAddr+"crack-seg/vision-inference/info/", requestOptions)

  $('#max-width-td').empty()
  $('#average-width-td').empty()
  $('#total-width-td').empty()

  $('#max-width-td').append(crack_info.real_max_width+"mm")
  $('#average-width-td').append(crack_info.average_crack_width+"mm")
  $('#total-width-td').append(crack_info.all_crack_length * ((localStorage.getItem("width")/448) + localStorage.getItem("height")/448)+"cm")

}

//post API AS JSON
async function postAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  return data
}