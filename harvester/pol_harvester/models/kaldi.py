from django.db.utils import OperationalError

from datagrowth.resources import KaldiNLResource as KaldiNL, KaldiAspireResource as KaldiEN


class KaldiNLResource(KaldiNL):

    def save(self, *args, **kwargs):
        # This is a tough cookie
        # Really not sure why at the first try the Postgres seems to be shutdown and with a second try it always works.
        # Tried some Postgres setting as well as reconnect packages all to no avail
        # For now we're simply retrying once and leave it at that
        try:
            super().save(*args, **kwargs)
        except OperationalError:
            super().save(*args, **kwargs)


class KaldiAspireResource(KaldiEN):

    def save(self, *args, **kwargs):
        # This is a tough cookie
        # Really not sure why at the first try the Postgres seems to be shutdown and with a second try it always works.
        # Tried some Postgres setting as well as reconnect packages all to no avail
        # For now we're simply retrying once and leave it at that
        try:
            super().save(*args, **kwargs)
        except OperationalError:
            super().save(*args, **kwargs)
