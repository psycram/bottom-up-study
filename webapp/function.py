from webapp.models.models import UserLectureProgress
from datetime import datetime, timedelta
from collections import defaultdict

def get_user_study_progress(user_id):
    # 解いたレクチャー数のカウント
    lecture_count = UserLectureProgress.query.filter_by(user_id=user_id).count()

    # レクチャーを解いた日付を取得し、重複を除いて降順に並べる
    solved_dates = (
        UserLectureProgress.query
        .filter_by(user_id=user_id)
        .with_entities(UserLectureProgress.solved_at)
        .distinct()
        .order_by(UserLectureProgress.solved_at.desc())
        .all()
    )

    # 日付リストだけに変換
    solved_dates = [entry.solved_at.date() for entry in solved_dates]

    # 連続勉強日数をカウント
    consecutive_days = 0
    for i in range(len(solved_dates) - 1):
        if i == 0:
            consecutive_days = 1
        if (solved_dates[i] - solved_dates[i + 1]).days == 1:
            consecutive_days += 1
        else:
            break  # 連続が途切れたら終了

    return lecture_count, consecutive_days



def get_last_week_activity(user_id):
    # 今日から1週間前までの範囲を定義
    today = datetime.today()
    one_week_ago = today - timedelta(days=6)  # 直近7日分

    # デフォルト値が0の辞書を用意し、日付ごとにカウント
    daily_activity = defaultdict(int)
    for i in range(7):
        date_key = (today - timedelta(days=i)).date()
        daily_activity[date_key] = 0  # 初期化

    # 1週間以内のユーザーの解答データを取得
    results = UserLectureProgress.query.filter(
        UserLectureProgress.user_id == user_id,
        UserLectureProgress.solved_at >= one_week_ago
    ).all()

    # 日ごとの説いた問題数をカウント
    for result in results:
        date_key = result.solved_at.date()
        daily_activity[date_key] += 1

    # 日付を昇順に並べてラベルとデータのリストを作成
    labels = []
    data = []
    for i in range(6, -1, -1):  # 昨日から過去へ
        date_key = (today - timedelta(days=i)).date()
        labels.append(date_key.strftime("%m/%d"))  # 日付ラベルをMM/DD形式に変換
        data.append(daily_activity[date_key])

    return labels, data
