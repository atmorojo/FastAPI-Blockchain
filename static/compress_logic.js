import Compress from "/static/compress.min.js";

const compressor		= new Compress();
const dataTransfer	= new DataTransfer();

let upload = document.getElementById("upload")
let img = document.getElementById("preview")

// Listen to file upload events.
upload.addEventListener("change",
  async function (evt) {
    const file		= evt.target.files[0];
    const newFile = await compressor.compress(file, {
      quality: 0.8,
      maxWidth: 500, // Image width will not exceed 500px.
    });

    // Display the image on the img element.
    dataTransfer.items.add(newFile);
    upload.files = dataTransfer.files;
    img.src=URL.createObjectURL(upload.files[0]);
  })
