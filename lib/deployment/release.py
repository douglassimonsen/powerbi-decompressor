import requests
import json
from pprint import pprint
from pathlib import Path
import git
from extract_library import __version__

access_token = "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"
repo_owner = "douglassimonsen"
repo_name = "powerbi-decompressor"
request_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
repo = git.Repo(search_parent_directories=True)


def create_release():
    release_notes = f"""
Automatic generated release for version {__version__}.
Some of the new updates:

{repo.head.commit.message}
    """.strip()  # can't do dedenting because the message is multiline
    requests.post(
        request_url,
        json={
            "tag_name": f"v{__version__}",
            "target_commitish": "main",
            "name": f"v{__version__}",
            "body": release_notes,
            "draft": False,
            "prerelease": False,
            "generate_release_notes": True,
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        },
    )


def add_wheel():
    x = requests.get(request_url + "/latest", headers={"Authorization": access_token})
    data = json.loads(x.text)
    if data["tag_name"] != f"v{__version__}":
        raise ValueError("The tag/release failed to generate")
    upload_url = data["upload_url"].split("{")[0] + "?name=extract_library.tar.gz"
    try:
        requests.post(
            upload_url,
            data=open(
                Path(__file__).parents[1] / f"dist/extract_library-latest.tar.gz", "rb"
            ).read(),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/zip",
            },
        )
    except requests.exceptions.ConnectionError:
        pass


def main():
    create_release()
    add_wheel()


if __name__ == "__main__":
    main()
