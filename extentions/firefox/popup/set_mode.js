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

browser.storage.local.get({'is_run': false, 'port': 8080})
.then((params) => {
  checkbox.checked = params.is_run
})

checkbox.addEventListener("change", (e) => {
  browser.storage.local.set({'is_run': e.target.checked})
})
