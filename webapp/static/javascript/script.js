document.addEventListener("DOMContentLoaded", function() {
  var form = document.getElementById("create-text"); // フォームのIDに置き換える
  form.onsubmit = function() {
    document.getElementById("loadingMessage").style.display = "block"; // メッセージを表示
  };
});

function start() {
  gapi.client.init({
      'apiKey': '', // ここにあなたのAPIキーを置き換えてください
      'discoveryDocs': ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
  }).then(function() {
      loadData();
  });
}

function loadData() {
  gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: 'YOUR_SPREADSHEET_ID', // あなたのスプレッドシートIDを置き換えてください
      range: 'B2:B5',
  }).then(function(response) {
      var range = response.result;
      if (range.values && range.values.length > 0) {
          appendDataToTable(range.values);
      } else {
          console.log('No data found.');
      }
  }, function(response) {
      console.log('Error: ' + response.result.error.message);
  });
}

function appendDataToTable(data) {
  var table = document.createElement('table');
  data.forEach(function(row) {
      var tr = document.createElement('tr');
      var td = document.createElement('td');
      td.textContent = row[0];
      tr.appendChild(td);
      table.appendChild(tr);
  });
  document.body.appendChild(table);
}

document.addEventListener('DOMContentLoaded', function() {
  gapi.load('client', start);
});
