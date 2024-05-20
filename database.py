from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config
from datetime import datetime, timedelta

DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, index=True)
    daily_requests = Column(Integer, default=config.DAILY_LIMIT)
    last_request_date = Column(DateTime, default=datetime.utcnow)
    subscription_status = Column(String, default='free')

def reset_daily_limits():
    current_time = datetime.utcnow()
    reset_time = current_time - timedelta(days=1)

    session = SessionLocal()
    users = session.query(User).filter(User.last_request_date < reset_time).all()
    for user in users:
        user.daily_requests = config.DAILY_LIMIT
        user.last_request_date = current_time
        session.add(user)
    session.commit()
    session.close()

def init_db():
    Base.metadata.create_all(bind=engine)
