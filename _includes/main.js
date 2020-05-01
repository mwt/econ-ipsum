var pcache = [];
var element = document.getElementById("np");
var np = 5;

/* Function makes request stores paragraphs in pcache */
function xhr(post) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      pcache.push(...xhttp.responseText.split("\n"))
      if (typeof post !== "undefined") {
        post();
      }
    }
  };
  xhttp.open("GET", "https://gfyahgphl9.execute-api.us-east-1.amazonaws.com/Econ-Ipsum?np=100", true);
  xhttp.send();
  return;
};

/* Replace text on page with first `np` elements of pcache */
function refreshText() {
  var tags = document.getElementsByClassName("post-content");
  var clone = tags[0].cloneNode(false);
  const pused = pcache.splice(0, np);
  clone.innerHTML = pused.join(" ");
  tags[0].parentNode.replaceChild(clone, tags[0]);
  return;
};

/* Event listener */
document.getElementById("generate").addEventListener("click", function (e) {
  e.preventDefault();
  np = parseInt(element.value);
  if (pcache.length >= np) {
    refreshText();
  } else if (np <= 100) {
    xhr(refreshText);
  }
}, false);

/* Prefetch */
xhr();