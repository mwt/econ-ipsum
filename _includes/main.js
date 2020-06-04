var pcache = [];
var element = document.getElementById("np");
var np = 5;
var niter = 1;

/* Function makes request stores paragraphs in pcache */
function xhr(post) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      niter += 1;
      pcache.push(...xhttp.responseText.split("\n"));
      if (typeof post !== "undefined") {
        post();
      }
    }
  };
  const fetchURL = `https://api.econu.me/v1/Econ-Ipsum?np=100&z=${niter}`;
  xhttp.open("GET", fetchURL, true);
  xhttp.send();
  return;
};

/* Replace text on page with first `np` elements of pcache */
function refreshText() {
  /* get the content an abstract elements */
  var acontent = document.getElementsByClassName("abstract");
  var pcontent = document.getElementsByClassName("post-content");
  /* copy the two elements */
  var aclone = acontent[0].cloneNode(false);
  var pclone = pcontent[0].cloneNode(false);
  /* take np elements and leave the rest in the cache */
  const pused = pcache.splice(0, np);
  /* store the first element in the abstract and the others in content */
  aclone.innerHTML = pused.shift();
  pclone.innerHTML = pused.join(" ");
  /* make actual replacements */
  acontent[0].parentNode.replaceChild(aclone, acontent[0]);
  pcontent[0].parentNode.replaceChild(pclone, pcontent[0]);
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