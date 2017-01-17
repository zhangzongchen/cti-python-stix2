"""Tests for the stix2 library"""

import datetime

import pytest
import pytz

import stix2

amsterdam = pytz.timezone('Europe/Amsterdam')
eastern = pytz.timezone('US/Eastern')


@pytest.mark.parametrize('dt,timestamp', [
    (datetime.datetime(2017, 1, 1, tzinfo=pytz.utc), '2017-01-01T00:00:00Z'),
    (amsterdam.localize(datetime.datetime(2017, 1, 1)), '2016-12-31T23:00:00Z'),
    (eastern.localize(datetime.datetime(2017, 1, 1, 12, 34, 56)), '2017-01-01T17:34:56Z'),
    (eastern.localize(datetime.datetime(2017, 7, 1)), '2017-07-01T04:00:00Z'),
])
def test_timestamp_formatting(dt, timestamp):
    assert stix2.format_datetime(dt) == timestamp


EXPECTED = """{
    "created": "2017-01-01T00:00:00Z",
    "id": "indicator--01234567-89ab-cdef-0123-456789abcdef",
    "labels": [
        "malicious-activity"
    ],
    "modified": "2017-01-01T00:00:00Z",
    "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    "type": "indicator",
    "valid_from": "1970-01-01T00:00:00Z"
}"""


def test_indicator_with_all_required_fields():
    now = datetime.datetime(2017, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc)

    indicator = stix2.Indicator(
        type="indicator",
        id="indicator--01234567-89ab-cdef-0123-456789abcdef",
        labels=['malicious-activity'],
        pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
        created=now,
        modified=now,
        valid_from=epoch,
    )

    assert str(indicator) == EXPECTED


# Minimum required args for an indicator
KWARGS = dict(
    labels=['malicious-activity'],
    pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
)


def test_indicator_autogenerated_fields():
    indicator = stix2.Indicator(**KWARGS)
    assert indicator.type == 'indicator'
    assert indicator.id.startswith('indicator--')
    assert indicator.created is not None
    assert indicator.modified is not None
    assert indicator.labels == ['malicious-activity']
    assert indicator.pattern == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator.valid_from is not None

    assert indicator['type'] == 'indicator'
    assert indicator['id'].startswith('indicator--')
    assert indicator['created'] is not None
    assert indicator['modified'] is not None
    assert indicator['labels'] == ['malicious-activity']
    assert indicator['pattern'] == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator['valid_from'] is not None


def test_indicator_type_must_be_indicator():
    with pytest.raises(ValueError) as excinfo:
        indicator = stix2.Indicator(type='xxx')

    assert "Indicators must have type='indicator'." in str(excinfo)


def test_indicator_id_must_start_with_indicator():
    with pytest.raises(ValueError) as excinfo:
        indicator = stix2.Indicator(id='my-prefix--')

    assert "Indicator id values must begin with 'indicator--'." in str(excinfo)


def test_indicator_required_field_labels():
    with pytest.raises(ValueError) as excinfo:
        indicator = stix2.Indicator()
    assert "Missing required field for Indicator: 'labels'." in str(excinfo)


def test_indicator_required_field_pattern():
    with pytest.raises(ValueError) as excinfo:
        # Label is checked first, so make sure that is provided
        indicator = stix2.Indicator(labels=['malicious-activity'])
    assert "Missing required field for Indicator: 'pattern'." in str(excinfo)
