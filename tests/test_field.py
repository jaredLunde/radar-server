from radar_server_legacy import fields


def test_field():
    print(fields.Field())
    assert 5 == 5


def test_field2():
    assert isinstance(fields.Field(), fields.Field)