let socket=io()
let form = document.getElementById("create_form")
let create2=document.getElementById("create_room")
function rooms2(x)
{
    if (!form.contains(x.target))
        create2.style.display = "none"
}
if(create2!=null)
    create2.addEventListener("click", rooms2)

let img1 = document.getElementById("img1")
let img2 = document.getElementById("img2")
let div1 = document.getElementById("div1")


let invite = document.getElementsByClassName("div")[0]
let div_invite=document.getElementsByClassName("form_div")[0]
function notifications(x)
{
    if (!div_invite.contains(x.target))
        div_invite.style.display = "none"
}
div_invite.addEventListener("click", notifications)
div_invite.style.display = "none"
if (img1 != null)
{
    img1.addEventListener("click", function () {
        div_invite.style.display="block"
    })
}

if (img2 != null)
{
    img2.addEventListener("click", function () {
        div_invite.style.display="block"
    })
}

let forms_invite=document.getElementsByClassName("notification-form")
function tap(x)
{
    let counter=0
    for (let i = 0; i < forms_invite.length;i+=1)
        if (forms_invite[i].contains(x.target))
        counter+=1
    if (counter === 0)
        div_invite.style.display = "none"
}
if(div_invite!=null)
    div_invite.addEventListener("click", tap)

socket.on("invite", function (list) {
    alert("You have been invited to the room" + list[2])
    let notification = document.getElementsByClassName("form_div")[0]
    notification.innerHTML += `<form action="/invite/handle/${list[0]}" class="notification-form" method="post">
      <h3> ${list[1]} invites you to join the room "${list[2]}"</h3>
      <div class="div">
    <button type="submit" value="Accept" name="Button">Accept</button>
    <button type="submit" value="Decline" name="Button">Decline</button>
  </div>
  </form>`
})
