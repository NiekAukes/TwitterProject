const splash = document.querySelector('.splash');

document.addEventListener('DOMContentLoaded', (e)=>{
    setTimeout((()=>{
        splash.classList.add('display-none');
    }), 2000);
})

function toggleCheck() {
    if(document.getElementById("myCheckbox").checked === true){
      document.getElementById("officialTweets").style.display = "block";
    } else {
      document.getElementById("officialTweets").style.display = "none";
    }
    if(document.getElementById("myCheckbox1").checked === true){
      document.getElementById("userTweets").style.display = "block";
    } else {
      document.getElementById("userTweets").style.display = "none";
    }
  }

  //FUNCTIONS FOR FADE-INS AND FADE-OUTS
function fade(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}

function unfade(element) {
  var op = 0.01;  // initial opacity
  element.style.display = 'block';
  var timer = setInterval(function () {
      if (op >= 1){
          clearInterval(timer);
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ")";
      op += op * 0.1;
  }, 10);
}

//FUNC FOR FADING IN AND OUT THE WEATHER ICON
//var slideSource = document.getElementById('weatherimage');
//slideSource.classList.toggle('fade');