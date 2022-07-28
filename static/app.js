let audioURL = "";
let trancriptionID = "";
let matches = [];

const transcribeBtn = document.getElementById("transcribe-btn");
var oOutput = document.getElementById("response");
var inputEl = document.getElementById("input-el");
var searchBtn = document.getElementById("search-btn");
var searchResponse = document.getElementById("search-response");
var againBtn = document.getElementById("again-btn");

function upload(form) {
  const formData = new FormData(form);

  var oReq = new XMLHttpRequest();
  oReq.open("POST", "upload", true);

  oReq.onload = function (oEvent) {
    if (oReq.status == 200) {
      oOutput.innerHTML = "Your file is ready to be transcribed!";
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

      transcribeBtn.setAttribute("disabled", "disabled");
      inputEl.style.display = "block";
      searchBtn.style.display = "block";
    } else {
      oOutput.innerHTML =
        "Error occurred when trying to transcribe your file.<br />";
    }
  };

  oOutput.innerHTML = "Transcribing!";
  console.log("Transcribing!");
  oReq.send(audioURL);
});

searchBtn.addEventListener("click", function () {
  search = inputEl.value;

  var oReq = new XMLHttpRequest();
  oReq.open("POST", "search", true);

  oReq.onload = function (oEvent) {
    if (oReq.status == 200) {
      oOutput.innerHTML = "Here is your search";
      response = JSON.parse(oReq.response);

      inputEl.style.display = "none";
      searchBtn.style.display = "none";
      searchResponse.style.display = "block";
      againBtn.style.display = "block";

      matches = response.match;
      displayMatches(matches);
    } else if (oReq.status == 204) {
      oOutput.innerHTML = "No match found, try again";
    } else {
      oOutput.innerHTML =
        "Error occurred when trying to search through your file.<br />";
    }
  };

  oOutput.innerHTML = "Searching!";
  console.log("Searching!");
  oReq.send(JSON.stringify({ search: search, id: trancriptionID }));
});

function displayMatches(matches) {
  let listItems = "<tr><th>Word</th><th>Count</th><th>$Time stamp</th></tr>";
  for (let i = 0; i < matches.length; i++) {
    listItems += `
        <tr>
            <th>${matches[i].text}</th>
            <th>${matches[i].count}</th>
            <th>${matches[i].timestamps}</th>
        </tr>
    `;
  }
  searchResponse.innerHTML = listItems;
}
