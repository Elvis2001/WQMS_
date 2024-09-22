from apscheduler.schedulers.background import BackgroundScheduler
import requests

def scheduled_task():
    try:
        response = requests.get('https://wqms-kwv1.onrender.com/run-model')
        print(response.json())
    except Exception as e:
        print(f"Failed to trigger script: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=10)
scheduler.start()
