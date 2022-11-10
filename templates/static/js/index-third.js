window.onload = function(){
  const location = "/templates/static/images/predicted/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  const resized_img_location = "/templates/static/images/resized/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpeg"
  predicted_img.src = location
  resized_img.src = resized_img_location
}

function toHome(){
  location.href="/";
}