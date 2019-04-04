function newComment(){

	var formData = new FormData(document.forms.postcomment);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href);
	xhr.send(formData);
	var name = document.getElementById('user');
	var commentBlock = document.getElementById('comments');
  var input = document.getElementById('text');
  if(input.value !== ""){
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
  var formData = new FormData();
  var parent = btn.parentNode;
  console.log(parent);
  formData.append('id',parent.getAttribute('id'));
  var mark = Number(parent.lastChild.innerHTML);
  if(parent.getAttribute('class')=='like-added'){
    parent.removeAttribute('class');
   
    mark--;
    parent.lastChild.innerHTML = " " + mark;
  }
  else{
    parent.setAttribute('class','like-added')
    mark++;
    parent.lastChild.innerHTML = " " + mark;
  }

  
  setTimeout(10000);
  var xhr = new XMLHttpRequest();
	xhr.open("POST","/restaurant/like");
	xhr.send(formData);
}