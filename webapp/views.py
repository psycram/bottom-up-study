from webapp import app,db
from flask import render_template,request,redirect,url_for,session,jsonify,Flask
from werkzeug.security import check_password_hash
<<<<<<< HEAD
from .models.models import User,Curriculum
from flask_login import login_user

# カスタムフィルタを定義
@app.template_filter('getattr')
def getattr_filter(obj, attr):
    return getattr(obj, attr, None)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        score = int(request.form['score'])
        if score <= 5:
            # カリキュラムをリストとして取得（例としてID 1, 2, 3のカリキュラムを取得）
            curriculums = db.session.query(Curriculum).filter(Curriculum.id.in_([1])).all()
            return render_template('pages/index.html', curriculums=curriculums)
        elif score > 5:
            # カリキュラムをリストとして取得（例としてID 1, 2, 3のカリキュラムを取得）
            curriculums = db.session.query(Curriculum).filter(Curriculum.id.in_([2])).all()
            return render_template('pages/index.html', curriculums=curriculums)
    return render_template('pages/index.html', curriculums="")


=======
from .models.models import User,Curriculum,Subject,Course
from flask_login import login_user

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/lecture/<int:course_id>')
def lecture(course_id):
    # course_id に基づいてコースを取得
    course = Course.query.get_or_404(course_id)
    
    # course のデータを渡す
    return render_template('pages/lecture.html', course=course)

@app.route('/roadmap')
def roadmap():
    subjects = Subject.query.all()  # 科目と関連するデータを取得
    return render_template('pages/roadmap.html', subjects = subjects)

@app.route('/curriculum', methods=['GET'])
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
>>>>>>> develop


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
        
@app.route('/signup')
def signup():
    return render_template('pages/signup.html')


@app.route('/mypage')
def mypage():
    return render_template('pages/mypage.html')



@app.route('/premium')
def premium():
    return render_template('pages/premium.html', output_text="")