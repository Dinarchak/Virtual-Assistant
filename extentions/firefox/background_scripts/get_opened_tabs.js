async function sendData() {

  const now = new Date()

  const data = await browser.storage.local.get({'is_run': false, 'port': 8080})

  console.log(data)

  if (data.is_run) {
    browser.tabs.query({currentWindow: true})
    .then((tabs) => {
      const tabs_list = []

      for (var tab of tabs) {
        tabs_list.push(tab.url)
      }

      return tabs_list
    }).then((tabs_list) => {
      fetch(`http://localhost:${data.port}/upd_stat`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({'tabs': tabs_list, "time": now.toLocaleString()})
      })
    })
  }
  setTimeout(sendData, 5000)
}

sendData()