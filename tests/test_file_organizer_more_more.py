import subprocess, sys
import file_organizer as org

def test_apply_moves_real_print(capsys, tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("hello")
    moves = org.plan_moves(tmp_path)
    counts = org.apply_moves(moves, simulate=False)
    out = capsys.readouterr().out
    assert "MOVE doc.txt -> Documents/doc.txt" in out
    assert counts["Documents"] == 1

def test_run_as_script(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("content")
    result = subprocess.run(
        [sys.executable, "file_organizer.py", str(tmp_path), "--simulate"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Summary" in result.stdout
