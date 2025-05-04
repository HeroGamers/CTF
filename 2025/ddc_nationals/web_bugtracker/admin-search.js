function runSearch() {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      alert("No token found. Please log in as admin.");
      window.location.href = "/login";
      return;
    }
    const searchField = document.getElementById('search-field').value;
    let query;

    if (searchField.trim() === "") {
      query = JSON.stringify([{"$match": {}}]);
    } else {
      query = JSON.stringify([{"$match": {"$or": [
        {"title": {"$regex": searchField, "$options": "i"}},
        {"description": {"$regex": searchField, "$options": "i"}}
      ]}}]);
    }

    fetch('/admin_search?query=' + encodeURIComponent(query), {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    })
    .then(res => {
      if (res.status === 401 || res.status === 403) {
        window.location.href = "/login";
        return Promise.reject("Redirecting to login...");
      }
      return res;
    })
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById('search-result');
      div.innerHTML = "";
      if (data.results && data.results.length > 0) {
        const table = document.createElement('table');
        const header = table.createTHead();
        const headerRow = header.insertRow(0);
        const keys = Object.keys(data.results[0]).filter(key => key !== "_id");
        keys.forEach((key, index) => {
          const cell = headerRow.insertCell(index);
          cell.outerHTML = `<th>${key}</th>`;
        });

        const tbody = table.createTBody();
        data.results.forEach(result => {
          const row = tbody.insertRow();
          keys.forEach((key, index) => {
            const cell = row.insertCell(index);
            cell.innerText = result[key];
          });
        });

        div.appendChild(table);
      } else {
        div.innerText = "No results";
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById('search-result').innerText = "Error running search.";
    });
  }

  window.onload = runSearch;



  function submitBug() {
    const title = document.getElementById('bug-title').value;
    const description = document.getElementById('bug-description').value;
    const severity = document.getElementById('bug-severity').value;

    fetch('/create_bug', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({ title, description, severity })
    })
    .then(res => {
      if (res.status === 401 || res.status === 403) {
        window.location.href = "/login";
        return Promise.reject("Redirecting to login...");
      }
      return res;
    })
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById('submit-result');
      if (data.success) {
        div.innerText = "Bug submitted successfully!";
      } else {
        div.innerText = "Error: " + (data.error || JSON.stringify(data));
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById('submit-result').innerText = "Error submitting bug.";
    });
  }

  function checkToken() {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      alert("You must be logged in. Token not found.");
      window.location.href = "/login";
    }
  }