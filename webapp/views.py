from webapp import app,db
from flask import render_template,request,redirect,url_for,session,jsonify,Flask
from werkzeug.security import check_password_hash
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