from deployment import export, release, tagger
import git


def main():
    repo = git.Repo(search_parent_directories=True).remote().push()[0]
    if tagger.main():  # we really only need to do the work if a new tag has been added
        export.main()
        release.main()


if __name__ == "__main__":
    main()
