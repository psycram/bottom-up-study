<<<<<<< HEAD
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
=======

  
  document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.lecture-section');
    let currentSectionIndex = 0;
  
    const resultModal = document.getElementById('result-modal');
    const resultText = document.getElementById('result-text');
    const nextButton = document.getElementById('next-button');
  
    // 最初のセクションを表示
    sections[currentSectionIndex].classList.add('active');
  
    // すべてのボタンにイベントリスナーを追加
    sections.forEach((section, index) => {
      const buttons = section.querySelectorAll('.answer');
      buttons.forEach(button => {
        button.addEventListener('click', () => {
          const isCorrect = button.getAttribute('data-correct') === 'true';  // 正解か不正解かを判定
  
          // 結果に応じてモーダルにメッセージを表示
          if (isCorrect) {
            resultText.textContent = '正解！';
            resultText.className = 'correct';
          } else {
            resultText.textContent = '不正解！';
            resultText.className = 'incorrect';
          }
  
          // モーダルを表示
          resultModal.style.display = 'block';
        });
      });
    });
  
    // 「次へ」ボタンを押したときの処理
    nextButton.addEventListener('click', () => {
      // モーダルを閉じる
      resultModal.style.display = 'none';
  
      // 現在のセクションを非表示
      sections[currentSectionIndex].classList.remove('active');
  
      // 次のセクションが存在する場合、表示
      if (currentSectionIndex + 1 < sections.length) {
        currentSectionIndex++;
        sections[currentSectionIndex].classList.add('active');
      }
    });
  });
  
>>>>>>> develop
