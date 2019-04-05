function newComment(){

	var formData = new FormData(document.forms.postcomment);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href);
	xhr.send(formData);
	var name = document.getElementById('user');
	var commentBlock = document.getElementById('comments');
  var input = document.getElementById('text');
  if(!name){
     $(".login-form").css("display", "block");
     $("body", "html").css("overflow", "hidden");
  }else if(input.value !== "" & input.value.length > 3){
    commentBlock.innerHTML += ` <div class="comments__card">
          <div class="comments__card-header">
            `+name.outerHTML+` 
          </div>
          <div class="comments__card-body">
            <blockquote>
              <p>`+input.value+`</p>
              <p class="comments__card-time">только что</p>
            </blockquote>
          </div>
        </div>`;
    input.value = "";
  }
}

function like(btn){
  // btn.removeAttribute('onclick');
  var formData = new FormData();
  var parent = btn.parentNode;
  formData.append('id',parent.getAttribute('id'));
  var mark = Number(parent.lastChild.innerHTML);
  var name = document.getElementById('user');
  if(name){
    if (parent.getAttribute('class') == 'like-added'){
      parent.removeAttribute('class');
      mark--;
    } else {
      parent.setAttribute('class', 'like-added')
      mark++;
    }
    parent.lastChild.innerHTML = " " + mark;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/restaurant/like");
    xhr.send(formData);
    setTimeout(function () {
      btn.setAttribute('onclick', 'like(this)');
    }, 200)
  }else{
      $(".login-form").css("display", "block");
      $("body", "html").css("overflow", "hidden");
      
  }
  
}