let audioURL = "";
let trancriptionID = "";

const transcribeBtn = document.getElementById("transcribe-btn");
var oOutput = document.getElementById("static_file_response");
var inputEl = document.getElementById("input-el");

function upload(form) {
  const formData = new FormData(form);

  var oReq = new XMLHttpRequest();
  oReq.open("POST", "upload", true);

  oReq.onload = function (oEvent) {
    if (oReq.status == 200) {
      oOutput.innerHTML = "Your File is ready to be transcribed!";
      response = JSON.parse(oReq.response);
      audioURL = response.url;
      transcribeBtn.removeAttribute("disabled");
    } else {
      oOutput.innerHTML =
        "Error occurred when trying to upload your file.<br />";
    }
  };

  oOutput.innerHTML = "Sending file!";
  console.log("Sending file!");
  oReq.send(formData);
}

transcribeBtn.addEventListener("click", function () {
  var oReq = new XMLHttpRequest();
  oReq.open("POST", "transcribe", true);

  oReq.onload = function (oEvent) {
    if (oReq.status == 200) {
      oOutput.innerHTML = "Your transcription is ready, find some words";
      response = JSON.parse(oReq.response);
      trancriptionID = response.id;
      console.log(trancriptionID);
    } else {
      oOutput.innerHTML =
        "Error occurred when trying to transcribe your file.<br />";
    }
  };

  oOutput.innerHTML = "Transcribing!";
  console.log("Transcribing!");
  oReq.send(audioURL);
});
