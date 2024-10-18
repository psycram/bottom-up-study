#テーブルの再作成
from webapp import app, db 

with app.app_context():
<<<<<<< HEAD
    db.drop_all()
    db.create_all()
=======
    # db.drop_all()
    db.create_all()
    
>>>>>>> develop
