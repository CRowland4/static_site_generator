from textnode import TextNode
from htmlnode import LeafNode


def main() -> None:
    node = TextNode("Hello World", "bold")
    print(node)
    return


if __name__ == "__main__":
    main()
