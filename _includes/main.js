/* Make warmup request */
var xmlHttp = new XMLHttpRequest();
xmlHttp.open("GET", "https://gfyahgphl9.execute-api.us-east-1.amazonaws.com/Econ-Ipsum?warmup", true);
xmlHttp.send(null);

/* Function makes request and puts data in post-content div */
function xhr() {
  var tags = document.getElementsByClassName("post-content");
  var clone = tags[0].cloneNode(false);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      clone.innerHTML = xhttp.responseText;
      tags[0].parentNode.replaceChild(clone, tags[0]);
    }
  };
  var element = document.getElementById("np");
  xhttp.open("GET", "https://gfyahgphl9.execute-api.us-east-1.amazonaws.com/Econ-Ipsum?np=" + element.value, true);
  xhttp.send();
  return;
};

/* Event listener */
document.getElementById("generate").addEventListener('click', function(e) {
  e.preventDefault();
  xhr();
}, false);