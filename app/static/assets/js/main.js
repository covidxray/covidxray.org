//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");
var covid = document.getElementById("covid");
var pneumonia = document.getElementById("pneumonia");
var normal = document.getElementById("normal");
var result = []
// Add event listeners
if (fileDrag != null) {
  fileDrag.addEventListener("dragover", fileDragHover, false);
  fileDrag.addEventListener("dragleave", fileDragHover, false);
  fileDrag.addEventListener("drop", fileSelectHandler, false);
  fileSelect.addEventListener("change", fileSelectHandler, false);
} 


function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");
var chartContainer = document.getElementById("chart-container");
var getColor = {
  'AB': '#FF0000',
  'BC': '#00FF00',
  'CL': '#FF4500', 
};

//========================================================================
// Main button events
//========================================================================

function submitImage() {
  // action for the submit button

  if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
    $("#confirm-modal").modal("show");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  // call the predict function of the backend
  predictImage(imageDisplay.src);
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  chartContainer.innerHTML = "";
  show(uploadCaption);
  result = []

  imageDisplay.classList.remove("loading");
}

function previewFile(file) {
  // show the preview of the image
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    imageDisplay.classList.remove("loading");
    chartContainer.innerHTML = "";
    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  hide(loader);
  if (data.result == "NOT DETECTED") {
    predResult.innerHTML = data.result + "<br><br>" + data.error;
    result = []
  } else {
    result = data.condition_similarity_rate
    predResult.innerHTML = data.case + "<br><br>" + data.types + "<br><br>" + data.prob;
    chart = Highcharts.chart('chart-container', {
      chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie'
      },
      title: {text: 'Condition rate'},
      tooltip: {pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
      accessibility: {
          point: {
              valueSuffix: '%'
          }
      },
      plotOptions: {
          pie: {
              allowPointSelect: true,
              cursor: 'pointer',
              dataLabels: {
                  enabled: true,
                  format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                  style: {
                      fontSize: 14
                  },
                  showInLegend: true

              }
          }
      },
      series: [{
          name: 'Brands',
          colorByPoint: true,
          data: [
            {
                name: "COVID-19",
                y: data.condition_similarity_rate[0].y,
                color: getColor['AB'],
                sliced: true,

            }, {
                name: 'NORMAL',
                y: data.condition_similarity_rate[1].y,
                color: getColor['BC'],
                sliced: true,
            }, {
                name: 'Pneumonia',
                y: data.condition_similarity_rate[2].y,
                color: getColor['CL'],
                sliced: true,
            },
          ]
      }]
  });
  }

  show(chartContainer);
  show(predResult);

}

function submitFormInformation() {
  if(result.length == 0) {
    $("#confirm-modal").modal("show");
    return false;
  } else {
    covid.value = result[0].y
    normal.value = result[1].y
    pneumonia.value = result[2].y
    clearImage()
    return true;

  }
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}