import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from WQMS import app
from WQMS.scheduler import scheduler
#from WQMS.routes import routes
#from WQMS.routes2 import routes2

# Load environment variables
load_dotenv()

# Register blueprints
#app.register_blueprint(routes)
#app.register_blueprint(routes2)

def scheduled_task():
    try:
        response = requests.get('https://wqms-kwv1.onrender.com/run-model')
        print(response.json())
    except Exception as e:
        print(f"Failed to trigger script: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=3)
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)#change to debug=True while deploying live
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
