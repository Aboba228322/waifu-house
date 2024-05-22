from flask import Flask, request, render_template
import hashlib
import config
from database import SessionLocal, User
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/notification', methods=['POST'])
def notification():
    try:
        data = request.form.to_dict()
        user_id = data.get('us_user_id')
        requests_count = int(data.get('us_requests_count'))
        amount = data.get('AMOUNT')
        merchant_order_id = data.get('MERCHANT_ORDER_ID')
        sign = data.get('SIGN')

        logger.info(f"Received notification: {data}")

        sign_check_str = f"{config.MERCHANT_ID}:{amount}:{config.SECRET_WORD_2}:{merchant_order_id}"
        sign_check = hashlib.md5(sign_check_str.encode()).hexdigest()

        logger.info(f"Sign Check Data: {sign_check_str}")
        logger.info(f"Calculated Signature: {sign_check}")
        logger.info(f"Received Signature: {sign}")

        if sign == sign_check:
            session = SessionLocal()
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.daily_requests += requests_count
                session.commit()
                logger.info(f"Updated user {user_id} requests: {user.daily_requests}")
            session.close()
            return 'YES'
        else:
            logger.error("Signature mismatch")
            return 'NO'
    except Exception as e:
        logger.exception("Error processing notification")
        return 'NO'

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/fail', methods=['GET'])
def fail():
    return render_template('fail.html')

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)
