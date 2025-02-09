from webapp import app,db
from flask import render_template,request,redirect,url_for,flash,session,jsonify
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from .models.models import User,Level,Unit,Subject,Course,UserLectureProgress,Lecture
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime,date,timedelta
from .function import get_user_study_progress,get_last_week_activity

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user,remember=True)
            session.permanent = True  # セッションの永続性を有効化
            return redirect('/')
        else:
            return render_template('pages/login.html',notLogin="間違えてますよ")
    else:
        return render_template('pages/login.html')
    
@app.route('/')
@login_required
def index():
    # ユーザーの進捗情報
    lecture_count, consecutive_days = get_user_study_progress(current_user.id)
    
    # 直近1週間の活動データ
    labels, data = get_last_week_activity(current_user.id)

    # テンプレートにデータを渡して表示
    return render_template('pages/index.html', 
                           lecture_count=lecture_count, 
                           consecutive_days=consecutive_days,
                           labels=labels, 
                           data=data)


@app.route('/lecture/<int:course_id>')
@login_required
def lecture(course_id):
    # course_id に基づいてコースを取得
    course = Course.query.get_or_404(course_id)
    
    # コースに紐づくすべての Lecture を取得
    lectures = Lecture.query.filter_by(course_id=course.id).order_by(Lecture.id).all()

    # course と lectures をテンプレートに渡す
    return render_template('pages/lecture.html', course=course, lectures=lectures)



@app.route('/roadmap')
def roadmap():
    # priorityの高い順にデータをソートして取得
    courses = db.session.query(Course).order_by(Course.priority.desc()).all()

    return render_template('pages/roadmap.html', courses = courses)


@app.route('/curriculum', methods=['GET'])
@login_required
def curriculum():
    # データベースから取得
    subjects = Subject.query.all()  # 科目と関連するデータを取得
    
    # タブ用にインデックス付きの科目リストを作成
    subject_names_with_index = list(enumerate([s.name for s in subjects]))

    return render_template(
        'pages/curriculum.html',
        subjects=subjects,
        subjectNamesWithIndex=subject_names_with_index
    )
   

# サインアップのルート
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        # 入力チェック
        if not username or not password or not repassword:
            flash('全てのフィールドを入力してください。', 'error')
            return redirect(url_for('signup'))

        if password != repassword:
            flash('パスワードが一致しません。', 'error')
            return redirect(url_for('signup'))

        # パスワードをハッシュ化して保存
        hashed_password = generate_password_hash(password)

        # ユーザーの追加
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('登録が完了しました！', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('エラーが発生しました。別のユーザー名を試してください。', 'error')
            return redirect(url_for('signup'))

    return render_template('pages/signup.html', notLogin='')

@app.route('/mypage')
@login_required
def mypage():
    return render_template('pages/mypage.html')


@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400
        
        solved_at = datetime.now()

        # 必要なデータを取得
        user_id = current_user.id  # ログインユーザーのIDを取得
        lecture_id = data.get('lecture_id')
        is_correct = data.get('is_correct')
        option_text = data.get('option_text')

        # 現在の周回数（最大attempt_number）を取得
        max_attempt = db.session.query(db.func.max(UserLectureProgress.attempt_number)).filter_by(
            user_id=user_id,
            lecture_id=lecture_id
        ).scalar()

        # 新しいattempt_numberを設定（最大attempt_numberがNoneの場合は1に設定）
        attempt_number = (max_attempt + 1) if max_attempt is not None else 1

        # 新しい進捗データをUserLectureProgressテーブルに追加
        progress = UserLectureProgress(
            user_id=user_id,
            lecture_id=lecture_id,
            is_correct=is_correct,
            attempt_number = attempt_number,
            option_text=option_text,
            solved_at=solved_at
        )

        db.session.add(progress)
        db.session.commit()

        # 成功した場合のレスポンス
        return jsonify({'success': True}), 200

    except Exception as e:
        # エラーが発生した場合
        db.session.rollback()  # データベースのロールバック
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/review-today')
@login_required
def review_today():
    # 今日の日付を取得
    today = date.today()
    
    # 今日解答済みのLectureのうち間違えたものだけを取得
    incorrect_lectures = UserLectureProgress.query.filter(
        UserLectureProgress.user_id == current_user.id,
        UserLectureProgress.is_correct == 0,
        UserLectureProgress.review < 1,
        UserLectureProgress.solved_at >= datetime(today.year, today.month, today.day)
    ).all()

    # 間違えたlectureのデータを取得し、重複を除去
    lecture_ids = {progress.lecture_id for progress in incorrect_lectures}
    lectures = Lecture.query.filter(Lecture.id.in_(lecture_ids)).all()

    # lecture.html テンプレートに、間違えたLectureだけを渡す
    return render_template('pages/review.html', lectures=lectures, review_mode=True)


@app.route('/mark-reviewed/<int:lecture_id>', methods=['POST'])
@login_required
def mark_reviewed(lecture_id):
    # 今日の特定Lectureに対するすべての解答データを取得
    progresses = UserLectureProgress.query.filter_by(
        user_id=current_user.id,
        lecture_id=lecture_id,
        is_correct=0
    ).all()

    if progresses:
        # すべての該当データのreviewカラムを1に更新
        for progress in progresses:
            progress.review += 1
        db.session.commit()  # 一度のコミットで全ての変更を保存
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "message": "解答データが見つかりません"}), 404



@app.route('/review-yesterday')
@login_required
def review_yesterday():
    # 昨日の日付の開始と終了を取得
    today = date.today()
    yesterday_start = datetime(today.year, today.month, today.day) - timedelta(days=1)
    yesterday_end = datetime(today.year, today.month, today.day)

    # 昨日解答済みのLectureのうち間違えたものだけを取得
    incorrect_lectures = UserLectureProgress.query.filter(
        UserLectureProgress.user_id == current_user.id,
        UserLectureProgress.is_correct == 0,
        UserLectureProgress.review < 2,
        UserLectureProgress.solved_at >= yesterday_start,
        UserLectureProgress.solved_at < yesterday_end
    ).all()

    # 間違えたlectureのデータを取得し、重複を除去
    lecture_ids = {progress.lecture_id for progress in incorrect_lectures}
    lectures = Lecture.query.filter(Lecture.id.in_(lecture_ids)).all()

    # review.html テンプレートに、昨日間違えたLectureだけを渡す
    return render_template('pages/review.html', lectures=lectures, review_mode=True)



@app.route('/continue')
@login_required
def continue_course():
    # 最後に解いたLectureProgressのレコードを取得
    latest_progress = UserLectureProgress.query.filter_by(
        user_id=current_user.id
    ).order_by(UserLectureProgress.solved_at.desc()).first()

    if not latest_progress:
        # まだ解答していない場合、リダイレクトなどの処理
        return redirect(url_for('index'))

    # 最新のlecture_idと結びついたcourse_idを取得
    course_id = latest_progress.lecture.course_id

    # 次のlecture_id以降のLectureを取得
    lectures = Lecture.query.filter(
        Lecture.course_id == course_id,
        Lecture.id > latest_progress.lecture_id
    ).order_by(Lecture.id).all()

    if not lectures:
        # すべてのレクチャーが終わった場合はリダイレクトなどの処理
        return redirect(url_for('index'))

    # 残りのlecturesをテンプレートに渡して表示
    return render_template('pages/lecture.html', lectures=lectures)




@app.route('/next-course')
@login_required
def load_next_course():
    # priorityが最も高いCourseを取得
    next_course = Course.query.order_by(Course.priority).first()

    if not next_course:
        # コースが存在しない場合はホームにリダイレクト
        print("aaa: No course found")
        return redirect(url_for('index'))

    print(f"Selected course ID: {next_course.id}, Priority: {next_course.priority}")

    # Courseに紐づくすべてのLectureを取得
    lectures = Lecture.query.filter_by(course_id=next_course.id).order_by(Lecture.id).all()

    if not lectures:
        # コース内にレクチャーがない場合もホームにリダイレクト
        print(f"bbb: No lectures found for course ID: {next_course.id}")
        return redirect(url_for('index'))

    # デバッグ: 取得したレクチャーの一覧を表示
    print("Lectures found:")
    for lecture in lectures:
        print(f"Lecture ID: {lecture.id}, Text: {lecture.text}")

    # コースとその講義リストをテンプレートに渡して表示
    return render_template('pages/lecture.html', lectures=lectures)

