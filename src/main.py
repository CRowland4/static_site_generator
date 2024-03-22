import os
import shutil
import textnode
from textnode import TextNode


def main() -> None:
    static = r".\static"
    public = r".\public"
    shutil.rmtree(public)
    os.mkdir(public)
    copy_contents(static, public)

    from_dir_path = r".\content"
    template_path = r".\template.html"
    dest_dir_path = r".\public"
    generate_pages_recursive(from_dir_path, template_path, dest_dir_path)

    return


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for item in os.listdir(dir_path_content):
        path_to_item = os.path.join(dir_path_content, item)
        if os.path.isfile(path_to_item) and path_to_item.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, item).replace(".md", ".html")
            generate_page(path_to_item, template_path, dest_path)
        elif os.path.isdir(path_to_item):
            generate_pages_recursive(path_to_item, template_path, dest_dir_path)

    return


def copy_contents(from_dir: str, to_dir: str) -> None:
    for item in os.listdir(from_dir):
        path_to_item = os.path.join(from_dir, item)
        if os.path.isdir(path_to_item):
            new_to_dir = os.path.join(to_dir, item)
            os.mkdir(new_to_dir)
            copy_contents(path_to_item, new_to_dir)
        else:
            shutil.copy(path_to_item, to_dir)
            print(f"Copied: {path_to_item} to {to_dir}")

    return


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown:
        markdown_contents = markdown.read()
    with open(template_path, "r") as template:
        template_contents = template.read()

    html = textnode.markdown_to_html_node(markdown_contents)
    page_title = extract_title(from_path).strip()
    html_content = html.to_html()
    template_contents = template_contents.replace("{{ Title }}", page_title)
    template_contents = template_contents.replace("{{ Content }}", html_content)

    with open(dest_path, "w") as final_html:
        final_html.write(template_contents)

    return


def extract_title(markdown: str) -> str:
    with open(markdown) as file:
        contents = file.readlines()

    for line in contents:
        if line.startswith("#") and line[1] != "#":
            return line.lstrip("# ")

    raise Exception(f"Missing single-# from file {markdown}")


if __name__ == "__main__":
    main()
