from flask import Flask, request, render_template
import hashlib
import config
from database import SessionLocal, User

app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def notification():
    data = request.form.to_dict()
    user_id = data.get('us_user_id')
    requests_count = int(data.get('us_requests_count'))
    amount = data.get('AMOUNT')
    sign = data.get('SIGN')


    sign_check_str = f"{config.MERCHANT_ID}:{amount}:{config.SECRET_WORD_2}:{user_id}"
    sign_check = hashlib.md5(sign_check_str.encode()).hexdigest()

    if sign == sign_check:
        session = SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.daily_requests += requests_count
            session.commit()
        session.close()
        return 'YES'
    return 'NO'

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/fail', methods=['GET'])
def fail():
    return render_template('fail.html')

@app.route('/test_notification', methods=['GET'])
def test_notification():
    return 'Notification endpoint is working!'

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)