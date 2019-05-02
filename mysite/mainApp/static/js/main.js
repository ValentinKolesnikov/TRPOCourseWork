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
  btn.removeAttribute('onclick');
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
  }
  else{
      $(".login-form").css("display", "block");
      $("body", "html").css("overflow", "hidden");
  }
  setTimeout(function () {
    btn.setAttribute('onclick', 'like(this)');
  }, 300)
}

function GetTime(btn){
  var formData = new FormData();
  formData.append('id', btn.id);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", document.location.href);
  xhr.send(formData);
  var checkstatus = setInterval(function(){
    if (xhr.status==200)
    {
    document.getElementsByClassName('time')[0].innerHTML = xhr.responseText;
    clearInterval(checkstatus);
    }
    else if(xhr.status!=0)
      clearInterval(checkstatus);
  }, 10);

}

function newposts(){
  var formData = new FormData();
  formData.append('cat',document.getElementsByClassName('ext-search__category')[0].value);
  if(formData.get('cat'))
    history.pushState(null, null, '?cat='+formData.get('cat'));
  else
    history.pushState(null, null, "/catalog/");

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/catalog/");
  xhr.send(formData);
  var checkstatus = setInterval(function(){
    if (xhr.status==200)
    {
      document.getElementsByClassName('kostil')[0].innerHTML = xhr.responseText;
      clearInterval(checkstatus);
    }
    
    else if(xhr.status!=0){
      clearInterval(checkstatus);
    }
     
  },10);

}

window.onload = function(){
  var now =new Date();
  var max = new Date(now.getFullYear, now.getMonth, now.getDay + 7);
  $('#date').datepicker({

    minDate: now,
  });
}


function GetTables(id, window, smoke)
{
  var formData = new FormData();
  formData.append('id',id);
  formData.append('window',window);
  formData.append('smoke',smoke);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/catalog/");
  xhr.send(formData);

  var checkstatus = setInterval(function(){
    if (xhr.status==200)
    {
      document.getElementsByClassName('order-card__tables-result')[0].innerHTML = xhr.responseText;
      clearInterval(checkstatus);
    }
    
    else if(xhr.status!=0){
      clearInterval(checkstatus);
    }
  },10);
}

function GetTimesTable(btn)
{
  var formData = new FormData();
  formData.append('idtable',btn.getAttribute("id"));
  var date = $('#date')[0].value;
  if ($('.selectedtable')[0])
    $('.selectedtable')[0].setAttribute('class', btn.getAttribute('class').replace(' selectedtable',''));
  btn.setAttribute('class', btn.getAttribute('class')+' selectedtable');
  if (date)
    formData.append('date', $('#date')[0].value);
  else{
    formData.append('date', '20.05.2019');
  }

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/catalog/");
  xhr.send(formData);

  var checkstatus = setInterval(function(){
    if (xhr.status==200)
    {
      document.getElementsByClassName('order-card__time-block')[0].innerHTML = xhr.responseText ;
      clearInterval(checkstatus);
    }
    
    else if(xhr.status!=0){
      clearInterval(checkstatus);
    }
  },10);
}
function ChangeDate(btn){
  console.log(btn.value);
}

function ChangeValue()
{
  var id = $('.order')[0].getAttribute('id');
  if(!id)
    id = $('.rest-order').getAttribute('id');
  console.log(id);
  var window = ($('#is-window')[0].checked);
  var smoke = ($('#is-smoke')[0].checked);
  document.getElementsByClassName('order-card__time-block')[0].innerHTML = "";


  GetTables(id, window, smoke);
}

function AddTables(){
  var formData = new FormData();
  formData.append('count', $('#id_count')[0].value);
  formData.append('smoke', $('#id_smoke')[0].checked);
  formData.append('window', $('#id_window')[0].checked);
  formData.append('counttables', $('#id_counttables')[0].value);
  formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]')[0].value);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/restaurant/tables/");
  xhr.send(formData);
  var block = $('.table')[0];
  for(i=0;i< Number($('#id_counttables')[0].value); i++)
    block.innerHTML+= '<p>'+ $('#id_count')[0].value+" " +$('#id_smoke')[0].checked+" "+$('#id_window')[0].checked+'</p>';
}

function DeleteTable(btn){
  var formData = new FormData();
  formData.append('id', btn.getAttribute('id'));
  formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]')[0].value);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/restaurant/tables/");
  xhr.send(formData);
  btn.parentNode.parentNode.removeChild(btn.parentNode);
}


function MakeOrder(btn){
  var name = document.getElementById('user');
  if(name){
    $('.order').css('display', 'block');
    $("body", "html").css("overflow", "hidden");
    var id = btn.getAttribute('id');
    $('.order')[0].setAttribute('id', id)
    var window = ($('#is-window')[0].checked);
    var smoke = ($('#is-smoke')[0].checked);

    GetTables(id,window,smoke);
  }else{
     $(".login-form").css("display", "block");
     $("body", "html").css("overflow", "hidden");
  }

  
}

var date = new Date();

function SelectTime(btn){
  if ($('#selectedtime')[0])
    $('#selectedtime')[0].removeAttribute('id');
  btn.setAttribute('id','selectedtime');
}

function SendOrder(){
  var dateorder = $('#date')[0];
  var tableorder = $('.selectedtable')[0];
  var timeorder = $('#selectedtime')[0];
  if(!dateorder||!tableorder||!timeorder)
    return;
  var formData = new FormData();
  formData.append('date', dateorder.value);
  formData.append('table', tableorder.id);
  formData.append('time', timeorder.innerHTML);
  formData.append('text', $('.order-card__offer')[0].value);
  formData.append('restaurant', $('.order')[0].getAttribute('id'))

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/catalog/");
  xhr.send(formData);
  if(!$('.rest-order')[0]){
    HideOrderForm();
  }
  else{
    $('.order-card__time-block')[0].innerHTML = "";
    $('.order-card__date')[0].value = "";
    $('.order-card__checkbox')[0].checked = false;
    $('.order-card__checkbox')[1].checked = false;
    $('.order-card__tables-result')[0].innerHTML = '';
    $('.order-card__offer')[0].value = '';
  }

  
}



function HideOrderForm() {
  $('.order').css('display', 'none');
  $("body", "html").css("overflow", "auto");
  $('.order-card__time-block')[0].innerHTML = "";


  

}