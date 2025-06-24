const err_block = document.querySelector("#error-content")
const err_text = document.querySelector("#error-content > p")
const checkbox = document.querySelector(".switch > input")

function showError(text) {
  err_block.classList.remove("hidden")
  err_text.innerHTML = text
}

function hideError() {
  err_block.classList.add("hidden")
  err_text.innerHTML = ""
}

function sendData() {

  const checkbox = document.querySelector(".switch > input")

  browser.tabs.query({currentWindow: true}, (tabs) => {
    for (var tab of tabs) {
      console.log(tab.url);
   }
  })

  // fetch('http://localhost:8080/?key="123"')
  // .then((resp) => {
  //   if (resp.status === 200) {
  //     hideError()
  //     return resp.text()
  //   } else {
  //     showError("Что-то пошло не так.")
  //   }
  // })
  // .then(text => alert(text))

  if (checkbox.checked)
    setTimeout(sendData, 5000)
}


checkbox.addEventListener("change", (e) => {
  if (e.target.checked) {
    sendData(e.target)
  }
})

if (checkbox.checked) {
  sendData(checkbox)
}