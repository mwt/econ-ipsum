function xhr() {
  var tags = document.getElementsByClassName("post-content");
  var clone = tags[0].cloneNode(false);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      clone.innerHTML = xhttp.responseText.match(/<p>.+<\/p>/i)[0];
      tags[0].parentNode.replaceChild(clone, tags[0]);
    }
  };
  var element = document.getElementById("np");
  var formData = new FormData(); 
  formData.append(element.name, element.value);
  xhttp.open("POST", "https://econ-ipsum.appspot.com/", true);
  xhttp.send(formData);
  
  return;
};


document.getElementById("generate").addEventListener('click', function(e) {
  e.preventDefault();
  xhr();
}, false);