
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
          var html = '';
          $.each(data, function(index, item) {
              html += '<p>' + item.name + '</p>';
            });
            html += ' ';
          t2.classList.add("show");
          $('#test').html(html);
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

// below this is top 10 common symptoms 
var add_div = document.getElementById("top")
var add_items = document.getElementsByTagName("a")

    var html = '';
    $.getJSON('/top', function(data){
        html += '<table>';
        var i = 0;
        $.each(data, function(index, item) {
            html += '<tr>';
            html += '<td>' + '<input type="checkbox" onclick="cbox' + `${i.toString()}`+ '()" ' +  'id="C'+ `${i.toString()}`+ '">' + '<label id="CL'+ `${i.toString()}`+ '"' + ' for="C'+ `${i.toString()}`+ '">' + item.name + '</label>' +'</td>' ;
            if(i%2==0){
                html += '</tr';
            }
            i++;
          });
        add_div.classList.add("show");
        $('#top').html(html);
    })

// below this is code to select from check boxes and add that to results array

// t2 = document.getElementById("test");

function cbox0() {
    var label = document.querySelector("label[for=C0").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}

function cbox1() {
    var label = document.querySelector("label[for=C1").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox2() {
    var label = document.querySelector("label[for=C2").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox3() {
    var label = document.querySelector("label[for=C3").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox4() {
    var label = document.querySelector("label[for=C4").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox5() {
    var label = document.querySelector("label[for=C5").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox6() {
    var label = document.querySelector("label[for=C6").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox7() {
    var label = document.querySelector("label[for=C7").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox8() {
    var label = document.querySelector("label[for=C8").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
function cbox9() {
    var label = document.querySelector("label[for=C9").textContent;
    $.getJSON('/append', {a: label}, function(data) {
    //     var html = '';
    //     $.each(data, function(index, item) {
    //         html += '<p>' + item.name + '</p>';
    //       });
    // t2.classList.add("show");
    //   $('#test').html(html);
    });
}
// below this is code for done button when user has selected all pre-given symptoms



// below this is bot working code that connects backend by calling api 

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "/static/Draken.png";
const PERSON_IMG = "/static/User.png";
const BOT_NAME = "   Dr. Swastik";
const PERSON_NAME = "You";

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


function first(){
  var end = false;
  var html = '';
  $.getJSON('/main', function(data) {
    html += '<table>';
    var i = 0;
    $.each(data, function(index, item) {
        html += '<tr>';
        html += '<td>' + '<input type="checkbox" onclick="cbox' + `${i.toString()}`+ '()" ' +  'id="C'+ `${i.toString()}`+ '">' + '<label for="C'+ `${i.toString()}`+ '">' + item.name + '</label>' +'</td>';

        // const newElement = document.createElement('input');
        // newElement.type = 'checkbox';
        // newElement.onclick = 'cbox' + `${i.toString()}` + '()';
        // newElement.id = 'C' + `${i.toString()}` + '';
        // console.log(newElement.id);
        // const oldElement = document.getElementById('C' + `${i.toString()}` + '');
        // oldElement.parentNode.replaceChild(newElement, oldElement);

        // //
        // const newLabel = document.createElement('label');
        // newLabel.for = 'C' + `${i.toString()}` + '';
        // newLabel.id = 'CL' + `${i.toString()}` + '';
        // newLabel.textContent = item.name;
        // const oldLabel = document.getElementById('CL' + `${i.toString()}` + '');
        // oldLabel.parentNode.replaceChild(newLabel, oldLabel);

        // //

        if(i%2==0){
            html += '</tr';
        }
        i++;


        if (item.name == "terminate"){
          console.log(item.disease);
          var txt = 'You probably have ';
          $.each(data,function(index,item){
            if(item.name == "terminate"){

            }
            else{
              txt += item.name + ' ';
            }
          });
          appendMessage(BOT_NAME, BOT_IMG, "left", txt);
          end = true;
        } 
      });
        // html += '<input type="button" onclick="first()" value="done">';
        if(end){
          console.log('Akinator off');
        }
        else{
          add_div.classList.add("show");
          $('#top').html(html);
        }
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
