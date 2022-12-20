import black
import black.report
import git
from pathlib import Path
import render_readme


def main():
    repo = git.Repo(Path(__file__).parents[1])
    staged_changes = [
        Path(x.a_path) for x in repo.index.diff("HEAD") if x.a_path.endswith(".py")
    ]
    cancel = False
    cancel |= render_readme.main()
    for change in staged_changes:
        ret = black.report.Report(quiet=True)
        black.reformat_one(
            change,
            fast=True,
            write_back=black.WriteBack.YES,
            mode=black.FileMode(),
            report=ret,
        )
        cancel |= bool(ret.change_count)
    if cancel:
        repo.index.add(staged_changes)
        repo.index.add(Path(__file__).parents[1] / "README.md")
    exit(cancel)


if __name__ == "__main__":
    main()
