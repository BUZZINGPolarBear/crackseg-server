window.onload = async function(){

  await postAPI(hostAddr+"crack-seg/run/detailed")
   $('#loading_status').empty();
   $('#loading_status').append('검출된 균열 분석중...')
  await getAPI(hostAddr + "crack-seg/vision-inference")
}

//post API AS JSON
async function postAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  console.log(res)
}

//get API
async function getAPI(host, options) {
  const res = await fetch(host, options)
  const data = res.json();
  console.log(res)
}