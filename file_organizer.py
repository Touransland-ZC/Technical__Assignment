%%writefile file_organizer.py

import argparse
from pathlib import Path
import shutil
import matplotlib.pyplot as plt


# myExtensions_Groups is a dict, each key represents a category which will map to a tuble representing the most popular extensions
# these are the most popular extensions, any new ext will be categorized as 'others' later
myExtensions_Groups = {
    "Images": ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "svg", "heic", "heif", "ico",),

    "Documents": ("pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx","txt", "md", "rtf", "csv", "tsv", "json","xml", "yaml", "yml", "ipynb", "tex",),

    "Videos": ("mp4", "mkv", "mov", "avi", "wmv", "flv", "webm", "m4v","3gp", "mpeg", "mpg", "ts", "m2ts", "ogv",),

    "Audio": ("mp3", "wav", "flac", "aac", "m4a", "ogg", "opus", "wma","aiff", "aif", "mid", "midi", "amr", "caf",),

    "Archives": ("zip", "rar", "7z", "tar", "gz", "bz2", "xz", "zst", "lz", "lzma","tgz", "tbz2", "txz",),

    "Code": ("py", "js", "ts", "jsx", "tsx","html", "css","c", "h", "cpp", "hpp", "cc", "cs", "java", "kt", "go", "rs", "rb", "php", "r", "jl", "m","sh", "bash", "zsh", "ps1", "bat", "pl", "lua", "sql","v", "sv", "vhd", "vhdl",),

    "eBooks": ("epub", "mobi", "azw", "azw3", "djvu", "fb2",),}




# flattening myExtensions_Groups to make the maping faster O(1)
EXT_TO_CATEGORY = {}
for cat, exts in myExtensions_Groups.items():
    for ext in exts:
        EXT_TO_CATEGORY[ext] = cat



# all the categories names, I will use this fixed order for a summary for the users
CATEGORIES = tuple([*myExtensions_Groups.keys(), "Others"])




# choose the file category based on the last file extension, and for unknown ext categorise them as 'Others'
def categorize(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    return EXT_TO_CATEGORY.get(ext, "Others")




# avoid overwriting existing files, so if a file name exists in its category folder, maybe from a previous run, then give it the same name but with a number.
# this happens in our real life, for ex when we past a file twice in folder, we find the new version's name have number between brackets like aaa.pdf, aaa (1).pdf, and so on.
# it handles if the file has multi suffix, like (archive.tar.gz)
# it handles the hidden files and the files with no extensions like the Readme
def safe_destination(dst_dir: Path, name: str) -> Path:
    p = Path(name)
    file_extensions = "".join(p.suffixes)

    if file_extensions:
        cut_extensions = len(p.name) - len(file_extensions)
        file_base_name = p.name[:cut_extensions]
    else:
        file_base_name = p.name

    new_file_path = dst_dir / (file_base_name + file_extensions)
    n = 1

    while new_file_path.exists():
        new_file_path = dst_dir / f"{file_base_name} ({n}){file_extensions}"
        n += 1
    return new_file_path





# scans the folder, without recursions or scannign subfolders
def scan_top_level(root: Path):
    for i in root.iterdir():
        if i.is_file():
            yield i




# it makes like a to-do list of the moves without moving the files
# it returns a list of tubles having the file source, distenation and category for moves
def plan_moves(root: Path):
    moves = []
    for f_src in scan_top_level(root):
        if not f_src.is_file():
            continue
        f_category = categorize(f_src)
        f_dst = safe_destination(root / f_category, f_src.name)
        moves.append((f_src, f_dst, f_category))
    return moves




# it can either executes or simulates the moves based on plan_moves.
# it returns counts per category.
def apply_moves(moves, simulate: bool = False):

    counts = {i_catergory: 0 for i_catergory in CATEGORIES}

    for f_src, f_dst, f_category in moves:

        if simulate:
            counts[f_category] += 1
            continue

        print(f"MOVE {f_src.name} -> {f_category}/{f_dst.name}")   # print each move
        try:
            f_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f_src), str(f_dst))                     # moving
            counts[f_category] += 1
        except Exception as e:
            print(f"SKIP {f_src.name} -> {f_category}/{f_dst.name} [error: {e}]")

    return counts




# printing a summary of the number of files moved per category.
def print_summary(counts):
    total = sum(counts.values())
    print("\n-.-_.-._-.-_.-._.-._.-.-\n\tSummary\n-.-_.-._-.-_.-._.-._.-.-")

    for i in CATEGORIES:
        print(f"{i}: {counts.get(i, 0)}")
    print(f"Total: {total}")




# it shows the summary in a form of a pie chart, if there are no files in the folder, then it will say No files to plot              
def show_summary_pie(counts, title="Files per category"):
    labels = [c for c in CATEGORIES if counts.get(c, 0)]
    sizes  = [counts[c] for c in labels]
    if not sizes:
        print("No files to plot", flush=True)
        return
    import matplotlib.pyplot as plt
    plt.ioff()  # make show() non-blocking in Colab
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%d", startangle=90)
    ax.axis("equal")
    ax.set_title(title)
    plt.tight_layout()
    plt.show()




# the command line interface.
# the user will have an option to simulation mode
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Organize files in a folder into Images, Documents, Videos, Audio, Archives, eBooks, Others based on extension.")

    p.add_argument("folder", type=Path, help="Path to the folder to organize")
    p.add_argument("--simulate", action="store_true", help="Show what would happen without moving files")
    p.add_argument("--plot-pie", action="store_true", help="Show a pie chart of the counts")

    return p.parse_args(argv)





def main(argv=None) -> int:
    args = parse_args(argv)
    root = args.folder

    if not root.exists() or not root.is_dir():
        print("The path must be an existing directory")
        return 2

    moves = plan_moves(root)
    counts = apply_moves(moves, simulate=args.simulate)

    print_summary(counts)

    if getattr(args, "plot_pie", False):
        show_summary_pie(counts)

    return 0



if __name__ == "__main__":
    raise SystemExit(main())
