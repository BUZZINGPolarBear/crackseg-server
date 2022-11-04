window.onload = function(){
  const location = "/templates/static/images/predicted/resized_"+ localStorage.getItem("pic_name").split(".")[0] + ".jpg"
  predicted_img.src = location
}