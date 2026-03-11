from platform_cli.commands import plan


def test_plan_module_has_app():
    assert plan.app is not None
