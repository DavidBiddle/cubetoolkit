import logging
import os.path

import magic

from django.db import models
import django.conf

logger = logging.getLogger(__name__)

class Role(models.Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=64, null=True)
    shortcode = models.CharField(max_length=8, null=True)

    # Can this role be added to the rota?
    rota = models.BooleanField(default=False)

    class Meta:
        db_table = 'Roles'

    def __unicode__(self):
        return self.name

class MediaItem(models.Model):
    """Media (eg. video, audio, html fragment?). Currently to be assoicated
    with events, in future with other things?"""

    def __init__(self, *args, **kwargs):
        if 'media_file' in kwargs and 'mimetype' not in kwargs:
            m = magic.Magic(mime=True)
            try:
                file_path = os.path.join(django.conf.settings.MEDIA_ROOT, kwargs['media_file'])
                kwargs['mimetype'] = m.from_file(file_path)
            except IOError:
                logging.error("Failed to determine mimetype of file {0}".format(file_path))
                kwargs['mimetype'] = "application/octet-stream"
        super(MediaItem, self).__init__(*args, **kwargs)

    media_file = models.FileField(upload_to="diary", max_length=256, null=True, blank=True)
    mimetype = models.CharField(max_length=64, null=True, blank=True)

    thumbnail = models.ImageField(upload_to="diary_thumbnails", max_length=256, null=True, blank=True)
    credit = models.CharField(max_length=64, null=True, blank=True, default="Internet scavenged")
    caption = models.CharField(max_length=128, null=True, blank=True)

    def validate_mime_type(self):
        # See lib/python2.7/site-packages/django/forms/fields.py for how to do
        # basic validation of PNGs / JPEGs
        pass

    def generate_thumbnail(self):
        # Can use django.core.files.images.get_image_dimensions...
        pass

    class Meta:
        db_table = 'MediaItems'

class Event(models.Model):

    name = models.CharField(max_length=256, blank=False)

    etype = models.ForeignKey('EventType', verbose_name='Event Type', related_name='etype', null=True, blank=True)
    duration = models.TimeField(null=True)

    cancelled = models.BooleanField(default=False)
    outside_hire = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    media = models.ManyToManyField(MediaItem, db_table='Event_MediaItems')
    # primary_media = models.ForeignKey('MediaItem', related_name='+', null=True, blank=True)
    # related_name="+" means that given MediaItem won't have a backlink to this model

    copy = models.TextField(max_length=8192, null=True, blank=True)
    copy_summary = models.TextField(max_length=4096, null=True, blank=True)

    terms = models.TextField(max_length=4096, null=True, blank=True)
    notes = models.TextField(max_length=4096, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Events'
    def __unicode__(self):
        return "%s (%d)" % (self.name, self.id)

class Showing(models.Model):

    event = models.ForeignKey('Event', related_name='showings')

    start = models.DateTimeField()

    booked_by = models.CharField(max_length=64, blank=False)

    @property
    def start_date(self):
        return self.start.date()

    extra_copy = models.TextField(max_length=4096, null=True)
    extra_copy_summary = models.TextField(max_length=4096, null=True)

    confirmed = models.BooleanField(default=False)
    hide_in_programme = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    discounted = models.BooleanField(default=False)

    # sales tables?

    # Rota entries
    roles = models.ManyToManyField(Role, through='RotaEntry')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Showings'

    def __unicode__(self):
        if self.start is not None and self.id is not None and self.event is not None:
            return "%s - %s (%d)" % (self.start.strftime("%H:%M %d/%m/%y"), self.event.name, self.id) 
        else:
            return "[uninitialised]"

    def reset_rota_to_default(self):
        """Clear any existing rota entries. If the associated event has an event
        type defined then apply the default set of rota entries for that type"""

        # Delete all existing rota entries (if any)
        self.rotaentry_set.all().delete()

        if self.event.etype is not None:
            # Add a rota entry for each role in the event type:
            for role in self.event.etype.roles.all():
                RotaEntry(role=role, showing=self).save()


class DiaryIdea(models.Model):
    month = models.DateField(editable=False)
    ideas = models.TextField(max_length=16384, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'DiaryIdeas'
    def __unicode__(self):
        return "%d/%d" % (self.month.month, self.month.year)

class EventType(models.Model):

    name = models.CharField(max_length=32, blank=False)
    shortname = models.CharField(max_length=32, blank=False)
    description = models.CharField(max_length=64, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Default roles for this event
    roles = models.ManyToManyField(Role, db_table='EventTypes_Roles')

    class Meta:
        db_table = 'EventTypes'

    def __unicode__(self):
        return self.name

class RotaEntry(models.Model):

    def __init__(self, *args, **kwargs):
        # Allow a template keyword arg to be supplied. If it is, copy rota
        # details across (except for the showing id, if that's set separately)
        if 'template' in kwargs:
            template = kwargs.pop('template')
        else:
            template = None

        super(RotaEntry, self).__init__(*args, **kwargs)

        if template:
            # Only use the showing from the template if one hasn't been set yet
            if self.showing is None:
                self.showing = template.showing
            self.role = template.role
            self.required = template.required
            self.rank = template.rank
            logger.info("Cloning rota entry from existing rota entry with role_id %d", template.role.pk)

    role = models.ForeignKey(Role)
    showing = models.ForeignKey(Showing)

    required = models.BooleanField(default=True)
    rank = models.IntegerField(default=1)

    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RotaEntries'

    def __unicode__(self):
        return "%s %d" % (unicode(self.role), self.rank)