from pathlib import Path
import file_organizer as org

def test_categorize_known_and_unknown(tmp_path):
    img = tmp_path / "a.JPG"
    txt = tmp_path / "b.txt"
    binf = tmp_path / "program.bin"
    img.write_text("x"); txt.write_text("x"); binf.write_bytes(b"\x00\x01")
    assert org.categorize(img) == "Images"
    assert org.categorize(txt) == "Documents"
    assert org.categorize(binf) == "Others"

def test_safe_destination_handles_duplicates_and_extensions(tmp_path):
    dst = tmp_path / "Images"; dst.mkdir()
    (dst / "photo.png").write_text("old")
    (dst / "archive.tar.gz").write_text("old")
    p1 = org.safe_destination(dst, "photo.png")
    p2 = org.safe_destination(dst, "archive.tar.gz")
    p3 = org.safe_destination(dst, ".gitignore")
    p4 = org.safe_destination(dst, "README")
    assert p1.name == "photo (1).png"
    assert p2.name == "archive (1).tar.gz"
    assert p3.name == ".gitignore"
    assert p4.name == "README"

def test_scan_top_level_skips_dirs(tmp_path):
    (tmp_path / "f1.txt").write_text("x")
    sub = tmp_path / "sub"; sub.mkdir()
    (sub / "nested.txt").write_text("y")
    names = {p.name for p in org.scan_top_level(tmp_path)}
    assert names == {"f1.txt"}

def test_plan_moves_uses_category_and_safe_destination(tmp_path):
    (tmp_path / "a.png").write_text("x")
    (tmp_path / "b.pdf").write_text("x")
    d = tmp_path / "Images"; d.mkdir()
    (d / "a.png").write_text("old")
    moves = org.plan_moves(tmp_path)
    trio = sorted([(src.name, dst.parent.name, dst.name) for src, dst, _ in moves])
    assert trio == [("a.png", "Images", "a (1).png"), ("b.pdf", "Documents", "b.pdf")]

def test_apply_moves_simulate_counts_only(tmp_path):
    (tmp_path / "a.mp4").write_text("x")
    (tmp_path / "b.xyz").write_text("x")
    moves = org.plan_moves(tmp_path)
    counts = org.apply_moves(moves, simulate=True)
    assert counts["Videos"] == 1
    assert counts["Others"] == 1
    assert (tmp_path / "a.mp4").exists()
    assert (tmp_path / "b.xyz").exists()

def test_apply_moves_real(tmp_path):
    (tmp_path / "a.mp3").write_text("x")
    moves = org.plan_moves(tmp_path)
    counts = org.apply_moves(moves, simulate=False)
    assert counts["Audio"] == 1
    assert not (tmp_path / "a.mp3").exists()
    assert (tmp_path / "Audio" / "a.mp3").exists()

def test_print_summary_output(capsys):
    counts = {c: 0 for c in org.CATEGORIES}
    counts["Images"] = 2; counts["Others"] = 1
    org.print_summary(counts)
    out = capsys.readouterr().out
    assert "Images: 2" in out
    assert "Others: 1" in out
    assert "Total: 3" in out

def test_show_summary_pie_handles_empty_counts(capsys):
    counts = {c: 0 for c in org.CATEGORIES}
    org.show_summary_pie(counts)
    out = capsys.readouterr().out
    assert "No files to plot" in out

def test_parse_args_flags():
    args = org.parse_args([str(Path(".")), "--simulate", "--plot-pie"])
    assert args.simulate is True
    assert args.plot_pie is True

def test_main_invalid_path_returns_2(tmp_path, capsys):
    missing = tmp_path / "nope"
    rc = org.main([str(missing)])
    assert rc == 2
    assert "must be an existing directory" in capsys.readouterr().out

def test_main_simulate_does_not_move(tmp_path):
    f = tmp_path / "doc.txt"; f.write_text("x")
    rc = org.main([str(tmp_path), "--simulate"])
    assert rc == 0
    assert f.exists()
