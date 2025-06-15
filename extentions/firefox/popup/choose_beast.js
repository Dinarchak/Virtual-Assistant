const btn = document.querySelector("#popup-content button")

btn.addEventListener("click", (e) => {
  fetch('http://localhost:8080/?key="123"')
  .then((resp) => {
    if (resp.status === 200) {
      return resp.text()
    }
    return "Ошибка соединения."
  })
  .then(text => alert(text))
})