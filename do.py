#テーブルの再作成
from webapp import app, db 

with app.app_context():
    # db.drop_all()
    db.create_all()


