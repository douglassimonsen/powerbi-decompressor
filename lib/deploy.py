from deployment import export, release, tagger


def main():
    if tagger.main():  # we really only need to do the work if a new tag has been added
        export.main()
        release.main()


if __name__ == "__main__":
    main()
