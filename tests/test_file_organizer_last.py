import file_organizer as org

def test_apply_moves_hits_line_91(capsys, tmp_path):
    # Create a file so apply_moves runs the normal MOVE branch
    f = tmp_path / "doc.txt"
    f.write_text("hello")
    moves = org.plan_moves(tmp_path)

    # Run in non-simulate mode so the MOVE print executes
    counts = org.apply_moves(moves, simulate=False)
    out = capsys.readouterr().out

    # Assert the MOVE line is in output
    assert "MOVE doc.txt -> Documents/doc.txt" in out
    assert counts["Documents"] == 1
