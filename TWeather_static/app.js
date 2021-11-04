//select splash screen
const splash = document.querySelector('.splash');

document.addEventListener('DOMContentLoaded', (e)=>{
    setTimeout((()=>{
        splash.classList.add('display-none');
    }), 2000);
})

//function to check togglebuttons
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