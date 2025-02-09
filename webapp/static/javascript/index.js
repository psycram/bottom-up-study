
document.addEventListener('DOMContentLoaded', function() {
  // テンプレートから埋め込まれたデータを取得
  const labels = JSON.parse(document.getElementById('chartLabels').textContent);
  const data = JSON.parse(document.getElementById('chartData').textContent);

  const ctx = document.getElementById('studyChart').getContext('2d');
  const studyChart = new Chart(ctx, {
    type: 'bar', // 棒グラフ
    data: {
      labels: labels,  // ラベルデータ
      datasets: [{
        label: '解いた問題数',
        data: data,  // データ
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});
