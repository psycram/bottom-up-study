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
        const optionText = button.getAttribute('data-option-text');  // 選択肢の内容

        // 非同期でデータを送信してreviewed_todayを1に設定
        markAsReviewed(lectureId);

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

  // 非同期でreviewed_todayを1に設定する関数
  function markAsReviewed(lectureId) {
    fetch(`/mark-reviewed/${lectureId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('解答データが更新されました。');
      } else {
        console.error('データの更新に失敗しました。');
      }
    })
    .catch(error => {
      console.error('ネットワークエラーが発生しました:', error);  // エラーの詳細をコンソールに表示
      alert(`ネットワークエラー: ${error.message}`);  // エラー内容をアラートに表示
    });
  }
});
