let socket=io()
let form = document.getElementById("create_form")
let create = document.getElementById("create")
let invite = document.getElementById("submit")
let error = document.getElementById("error")
if (error == null)
{
    create.style.display = "none"
}
invite.addEventListener("click", function () {
    create.style.display="flex"
})
create.addEventListener("click", function (x) {
    if (!form.contains(x.target))
        create.style.display = "none"
})

let attach = document.getElementById("Attach")
let file = document.getElementById("file")
attach.addEventListener("click", function () {
    file.click()
})

socket.on("message", function (list) {
    let messages = document.getElementsByClassName("messages")[0]
  if (list[3]) {
      console.log(1)
        messages.innerHTML += `
    <div class="item">
        <div class="main">
          <h3>${list[1]}</h3>
          <p>${list[2]}</p>
          <img src="/get/${list[3]}" alt="" style="width: 100px;">
        </div>
        <div class="img">
          <a href="/del/message/${list[4]}/${list[0]}"><img src="/static/Icons/bin.png" alt="hello" class="bin"></a>
        </div>
      </div>`}
  else {
    console.log(2)
        messages.innerHTML += `
    <div class="item">
        <div class="main">
          <h3>${list[1]}</h3>
          <p>${list[2]}</p>
        </div>
        <div class="img">
          <a href="/del/message/${list[4]}/${list[0]}"><img src="/static/Icons/bin.png" alt="hello" class="bin"></a>
        </div>
      </div>`
    }
})

socket.on("delete", function (list) {
  let url = window.location.href
  let lest = url.split("/")
  let len=lest.length
  let room_id =parseInt(lest[len-1])
  if (room_id === list[1])
  {
    let messages = document.getElementsByClassName("item")
    messages[list[0]-1].remove()
  }
})