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

  function handleGetTime(ip, btn) {
    sendCommand('/api/get_time', ip, function (data) {
      btn.closest('tr').querySelector('td:nth-child(3)').innerText = data.time
    })
  }

  function handleRefresh() {
    location.reload()
  }

  // Polling function to periodically check terminal status
  function pollTerminalStatus() {
    fetch('/api/get_terminal_statuses')
      .then((response) => response.json())
      .then((data) => {
        data.terminals.forEach((terminal) => {
          const row = document.querySelector(`tr[data-ip="${terminal.ip}"]`)
          if (row) {
            const statusCell = row.querySelector('td:nth-child(2)')
            if (terminal.status === 'Online') {
              statusCell.innerHTML = '<span class="badge bg-success">Online</span>'
            } else {
              statusCell.innerHTML = '<span class="badge bg-danger">Offline</span>'
            }
          }
        })
      })
      .catch((err) => console.error('Error updating status:', err))
  }

  // Polling every 10 seconds (adjust the time as needed)
  setInterval(pollTerminalStatus, 10000)

  function handleGetTime(ip, btn) {
    sendCommand('/api/get_time', ip, function (data) {
      const timeCell = btn.closest('tr').querySelector('td:nth-child(3)')
      if (timeCell) {
        timeCell.innerText = data.time || '—' // Ensure proper formatting if no time is returned
      }
    })
  }