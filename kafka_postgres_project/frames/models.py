from django.db import models
from datetime import datetime

class Frame(models.Model):
    frame_id = models.AutoField(primary_key=True)
    frame_data = models.TextField()
    timestamp = models.BigIntegerField()

    class Meta:
        db_table = 'frames'

    def __str__(self):
        return f"Frame {self.frame_id} at {self.get_formatted_timestamp()}"

    def get_formatted_timestamp(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
