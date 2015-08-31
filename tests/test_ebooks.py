import datetime
import os
import pytest

from freezegun import freeze_time

from config import Config
from wrangler.ebooks import EbooksText

@pytest.fixture
def cleandir(tmpdir):
    tmpdir.chdir()

@pytest.mark.usefixtures('cleandir')
def test_update_required(tmpdir):
    e = EbooksText(Config)
    assert e._update_required()

@pytest.mark.usefixtures('cleandir')
def test_update_required_if_timestamp(tmpdir):
    e = EbooksText(Config)
    e._write_timestamp()
    assert not e._update_required()

@pytest.mark.usefixtures('cleandir')
def test_update_required_after_12_hours(tmpdir):
    e = EbooksText(Config)
    e._write_timestamp()
    with freeze_time(datetime.datetime.now() + datetime.timedelta(hours=13)):
        assert e._update_required()
