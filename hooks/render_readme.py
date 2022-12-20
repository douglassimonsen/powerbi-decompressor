from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import jinja2

ROOT_FOLDER = Path(__file__).parents[1]


def empty_toc(folder, toc):
    page = toc.find("ul")
    for reference in page.find_all("a"):
        reference["href"] = folder + "/README.md" + reference["href"]

    full_toc = toc.new_tag("ul")
    full_toc_li = toc.new_tag("li")
    full_toc_link = toc.new_tag("a")
    full_toc_link["href"] = folder + "/README.md"
    full_toc_link.string = folder

    full_toc_li.append(full_toc_link)
    full_toc_li.append(toc.find("ul"))
    full_toc.append(full_toc_li)
    return full_toc


def main():
    sub_tocs = []
    for folder in ["lib", "load_to_db", "visualizer"]:
        with open(ROOT_FOLDER / folder / "README.md") as f:
            readme = f.read()
        md = markdown.Markdown(extensions=["toc"])
        md.convert(readme)
        toc = BeautifulSoup(md.toc, "xml")

        sub_tocs.append(empty_toc(folder, toc))

    final_toc = toc.new_tag("div")
    final_toc["style"] = "border:1px solid; max-width: 400px"
    toc_title = toc.new_tag("u")
    toc_title.string = "Table of Contents"
    final_toc.append(toc_title)
    final_toc_list = toc.new_tag("ul")
    final_toc.append(final_toc_list)
    for sub_toc in sub_tocs:
        li = toc.new_tag("li")
        final_toc_list.append(sub_toc)

    with open(ROOT_FOLDER / "README_template.md") as f:
        template = jinja2.Template(f.read())

    output = template.render(toc=final_toc.prettify())

    try:
        with open(ROOT_FOLDER / "README.md") as f:
            old_version = f.read()
        if output == old_version:
            return 0
    except FileNotFoundError:
        pass

    with open(ROOT_FOLDER / "README.md", "w") as f:
        f.write(output)
    return 1


if __name__ == "__main__":
    print(main())
