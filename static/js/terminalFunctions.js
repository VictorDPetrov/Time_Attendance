function sendCommand(endpoint, ip, callback) {
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip })
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert(data.message || 'Success')
          if (callback) callback(data)
        } else {
          alert(data.message || 'Failed')
        }
      })
      .catch((err) => alert('Error: ' + err))
  }

  function handlePing(ip) {
    sendCommand('/api/ping', ip)
  }

  function handleReboot(ip) {
    if (confirm('Are you sure you want to reboot the device?')) {
      sendCommand('/api/reboot', ip)
    }
  }

  function handleSetTime(ip) {
    sendCommand('/api/set_time', ip)
  }

  function handleRefresh() {
    location.reload()
  }

  function handleUpload(ip) {
    sendCommand('/api/ping', ip)
  }

  function handleGetTime(ip, btn) {
    sendCommand('/api/get_time', ip, function (data) {
      const timeCell = btn.closest('tr').querySelector('td:nth-child(3)')
      if (timeCell) {
        timeCell.innerText = data.time || '—' // Ensure proper formatting if no time is returned
      }
    })
  }