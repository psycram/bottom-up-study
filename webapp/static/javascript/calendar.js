// JavaScriptでFullCalendarを設定
document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',  // 月表示
    locale: 'ja',  // 日本語設定
    headerToolbar: {
      left: 'prev,next today',
      center: 'title'
    },
    events: [
      { title: 'イベント1', start: '2024-10-01' },
      { title: 'イベント2', start: '2024-10-07', end: '2024-10-10' },
      { title: 'イベント3', start: '2024-10-15T10:30:00', end: '2024-10-15T12:30:00' }
    ],
    dateClick: function(info) {
      // 日付をクリックしたときのモーダル表示
      document.getElementById('modalDate').innerText = `選択した日付: ${info.dateStr}`;
      document.getElementById('modal').style.display = 'flex';
    }
  });
  calendar.render();

  // モーダルの閉じる処理
  const modal = document.getElementById('modal');
  document.getElementById('closeModal').onclick = function() {
    modal.style.display = 'none';
  };
});
