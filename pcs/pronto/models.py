import json
import datetime

from django.db import models
from django.utils import timezone


class Pronto(models.Model):
    pronto_id = models.TextField()

    release = models.TextField(null=True, blank=True)
    feature = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    build = models.TextField(null=True, blank=True)
    severity = models.TextField(null=True, blank=True)
    responsible_person = models.TextField(max_length=50, null=True, blank=True)
    status = models.TextField(null=True, blank=True)

    transfer_from = models.TextField(null=True, blank=True)
    transfer_to = models.TextField(null=True, blank=True)

    rca_state = models.TextField(null=True, blank=True)

    reported_date = models.DateTimeField('Reported Date', null=True, blank=True)
    rft_date = models.DateTimeField('RFT Date', null=True, blank=True)
    in_date = models.DateTimeField('In Date', null=True, blank=True)
    out_date = models.DateTimeField('Out Date', null=True, blank=True)
    root_cause_found_date = models.DateTimeField('Root Cause Found Date', null=True, blank=True)

    is_top = models.TextField(default="false", null=True, blank=True)

    group_idx = models.TextField(null=True, blank=True)

    def was_reported_recently(self):
        now = timezone.now()
        if self.reported_date:
            return now - datetime.timedelta(days=7) < self.reported_date < now

    was_reported_recently.admin_order_field = 'pub_date'
    was_reported_recently.boolean = True
    was_reported_recently.short_description = 'Published recently?'

    def to_json(self):
        return json.dumps(dict([(attr, getattr(self, attr))
                                for attr in [f.name for f in self._meta.fields]]), cls=DateEncoder)

    def time_rft(self):
        if self.rft_date:
            return (self.rft_date - self.in_date).days
        else:
            return (self.out_date - self.in_date).days

    def time_test(self):
        if self.rft_date:
            return (self.out_date - self.rft_date).days
        else:
            return (self.out_date - self.out_date).days

    def __str__(self):
        return self.pronto_id
