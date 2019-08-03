from barrier.configure import main as configure


def test_run_without_arguments(cli_runner):
    """Should require expected arguments."""
    result = cli_runner.invoke(configure)
    assert result.exit_code == 2
