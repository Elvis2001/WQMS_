from datetime import datetime
from WQMS import db

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    tds = db.Column(db.Float)
    turbidity = db.Column(db.Float)

    def __repr__(self):
        return (f"<SensorData(timestamp={self.timestamp}, temperature={self.temperature}, "
                f"tds={self.tds}, turbidity={self.turbidity})>")
