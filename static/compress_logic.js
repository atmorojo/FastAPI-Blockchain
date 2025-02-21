import Compress from "/static/compress.min.js";

async function compress_file(evt) {
  const dataTransfer	= new DataTransfer();
  const compressor	= new Compress();

  let img	= document.getElementById("preview")

  // Listen to file upload events.
  const file		= evt.target.files[0];
  const newFile = await compressor.compress(file, {
    quality: 0.8,
    maxWidth: 500, // Image width will not exceed 500px.
  });

  // Display the image on the img element.
  dataTransfer.items.add(newFile);
  upload.files = dataTransfer.files;
  img.src=URL.createObjectURL(upload.files[0]);
}

document.getElementById("upload").addEventListener("change", compress_file);
