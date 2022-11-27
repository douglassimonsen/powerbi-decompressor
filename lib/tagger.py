import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent)

from extract_library import __version__
import git

possible_tag = "extract-lib-v" + __version__

repo = git.Repo()
if possible_tag not in repo.tags:
    tag = repo.create_tag(
        possible_tag, message=f"Automatic Tag for release: {possible_tag}"
    )
    repo.remotes.origin.push(tag)
