function newComment(){

	var formData = new FormData(document.forms.postcomment);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href);
	xhr.send(formData);
	var name = document.getElementById('user');
	var commentBlock = document.getElementById('comments');
	var input = document.getElementById('text');
	commentBlock.innerHTML +=` <div class="card">
        <div class="card-header">
          `+name.outerHTML+` только что
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <p>`+input.value+`</p>
          </blockquote>
        </div>
      </div>`;
  input.value = "";
}
function like(btn){
  var formData = new FormData();
  var parent = btn.parentNode;
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