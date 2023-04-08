const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "/static/Draken.png";
const PERSON_IMG = "/static/User.png";
const BOT_NAME = "   Dr. Swastik";
const PERSON_NAME = "You";


var input = document.getElementById("search-input");
var dropdown = document.getElementById("results");
var dropdownItems = dropdown.getElementsByTagName("p");

input.addEventListener("input",function() {
  if (input.value.length > 0){
    var query = $(this).val();
    $.getJSON('/search', {q: query}, function(data) {
      var html = '';
      $.each(data, function(index, item) {
        html += '<p>' + item.name + '</p>';
      });
      for (var i = 5; i < dropdownItems.length; i++) {
    dropdownItems[i].style.display = "block";
  }
  
    dropdown.classList.add("show");
    $('#results').html(html);

    for (let i = 0; i < dropdownItems.length; i++) {
      dropdownItems[i].addEventListener("click", function() {
        // change color of text within the p tag
        this.style.color = "green";
    
        // log the text content of the clicked p tag
        console.log(this.textContent);

        var label = this.textContent;

        t2 = document.getElementById("test");

        $.getJSON('/append', {a: label}, function(data) {
          if(data == null){
            
          }
          else{
            var txt = 'There is a chance that you have ';
            $.each(data, function(index, item) {
                txt += item.name + '  ';
              });
              appendMessage(BOT_NAME, BOT_IMG, "left", txt);
            }
        });
      });
    }
      
    });
  } else{
    for (var i = 0; i < dropdownItems.length; i++) {
    dropdownItems[i].style.display = "block";
  }
    dropdown.classList.remove("show");
  }
  
});



// above it implementing live search 



// below this is bot working code that connects backend by calling api 



msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  botResponse(msgText);
});

function botResponse(rawText) {

  // Bot Response
  $.get("/response", { msg: rawText }).done(function (data) {
    console.log(rawText);
    console.log(data);
    const msgText = data;
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);

  });

}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function get(selector, root = document) {
    return root.querySelector(selector);
  }

  function appendMessage(name, img, side, text) {
    //   Simple solution for small apps
    const msgHTML = `
<div class="msg ${side}-msg">
<div class="msg-img" style="background-image: url(${img})"></div>

<div class="msg-bubble">
  <div class="msg-info">
    <div class="msg-info-name">${name}</div>
    <div class="msg-info-time">${formatDate(new Date())}</div>
  </div>

  <div class="msg-text">${text}</div>
</div>
</div>
`;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }
