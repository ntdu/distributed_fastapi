from umongo import Document, fields
from datetime import datetime


class BaseDateTimeModel(Document):
    updated_at = fields.DateTimeField()
    created_at = fields.DateTimeField()

    class Meta:
        abstract = True

    def pre_insert(self):
        self.updated_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.created_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    def pre_update(self):
        self.updated_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
