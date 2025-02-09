document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.lecture-section');
  let currentSectionIndex = 0;

  const resultModal = document.getElementById('result-modal');
  const resultText = document.getElementById('result-text');
  const nextButton = document.getElementById('next-button');

  // 最初のセクションを表示
  sections[currentSectionIndex].classList.add('active');

  // すべてのボタンにイベントリスナーを追加
  sections.forEach((section) => {
    const buttons = section.querySelectorAll('.answer');
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        const isCorrect = button.getAttribute('data-correct') === 'true';  // 正解か不正解かを判定
        const lectureId = button.getAttribute('data-lecture-id');  // LectureID
        // const userId = button.getAttribute('data-user-id');  // ユーザーID
        const optionText = button.getAttribute('data-option-text');  // 選択肢の内容
        // const solvedAt = new Date().toISOString();  // 解答日時

        // 非同期でデータを送信
        sendAnswerData(lectureId, isCorrect, optionText);

        // 結果に応じてモーダルにメッセージを表示
        resultText.textContent = isCorrect ? '正解！' : '不正解！';
        resultText.className = isCorrect ? 'correct' : 'incorrect';
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

  // 非同期で解答データを送信する関数
  function sendAnswerData(lectureId, isCorrect, optionText) {
    fetch('/submit-answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // user_id: userId,
        lecture_id: lectureId,
        is_correct: isCorrect,
        option_text: optionText,
        // solved_at: solvedAt  // 解答日時
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('解答データが送信されました。');
      } else {
        console.error('解答データの送信に失敗しました。');
      }
    })
    .catch(error => {
      console.error('ネットワークエラーが発生しました:', error);  // エラーの詳細をコンソールに表示
      alert(`ネットワークエラー: ${error.message}`);  // エラー内容をアラートに表示
    });
    
  }
});


