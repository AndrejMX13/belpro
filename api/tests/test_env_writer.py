from pathlib import Path
from utils.env_writer import write_env_key


def test_creates_file_with_new_key(tmp_path):
    env = tmp_path / ".env"
    result = write_env_key("FOO", "bar", env)
    assert result is True
    assert "FOO=bar" in env.read_text()


def test_appends_key_to_existing_file(tmp_path):
    env = tmp_path / ".env"
    env.write_text("EXISTING=value\n")
    write_env_key("FOO", "bar", env)
    content = env.read_text()
    assert "EXISTING=value" in content
    assert "FOO=bar" in content


def test_updates_existing_key_in_place(tmp_path):
    env = tmp_path / ".env"
    env.write_text("FOO=old\nBAR=keep\n")
    write_env_key("FOO", "new", env)
    content = env.read_text()
    assert "FOO=new" in content
    assert "FOO=old" not in content
    assert "BAR=keep" in content


def test_does_not_duplicate_key(tmp_path):
    env = tmp_path / ".env"
    env.write_text("FOO=old\n")
    write_env_key("FOO", "new", env)
    assert env.read_text().count("FOO=") == 1


def test_preserves_comments(tmp_path):
    env = tmp_path / ".env"
    env.write_text("# comment\nFOO=old\n")
    write_env_key("FOO", "new", env)
    assert "# comment" in env.read_text()


def test_returns_false_on_unwritable_path():
    result = write_env_key("FOO", "bar", Path("/no/such/dir/.env"))
    assert result is False
