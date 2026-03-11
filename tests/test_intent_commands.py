from platform_cli.commands import intent


def test_intent_module_has_app():
    assert intent.app is not None
