from htmlnode import LeafNode
import re


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f'TextNode(text="{self.text}", text_type="{self.text_type}", url="{self.url}")'


def text_node_to_html(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(text_node.text)
        case "bold":
            return LeafNode(text_node.text, "b")
        case "italic":
            return LeafNode(text_node.text, "i")
        case "code":
            return LeafNode(text_node.text, "code")
        case "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unexpected text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list, text_type: str, delimiter: str) -> list:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        else:
            new_nodes.append(create_styled_nodes_from_node(node, text_type, delimiter))

    return new_nodes


def create_styled_nodes_from_node(node: TextNode, text_type: str, delimiter: str) -> list:
    """Transforms a raw TextNode (of text_type of "text") that contains text with valid Markdown syntax for non-nested
    bold, italics, or inline code formatting into a new TextNode of the appropriate type."""
    if node.text.count(delimiter) % 2 != 0:  # Valid markdown must contain an even number of delimiters
        raise Exception(f"Invalid markdown syntax for text: {node.text}")
    if node.text_type != "text":
        return [node]

    result_nodes = []
    raw_tokens = []
    styled_tokens = []
    styled_flag = False

    tokens = node.text.split()
    for token in tokens:
        if token.startswith(delimiter) and raw_tokens:
            raw_text = " ".join(raw_tokens)
            raw_tokens.clear()
            result_nodes.append(TextNode(raw_text, "text", node.url))
            styled_flag = True
            styled_tokens.append(token.lstrip(delimiter))
        elif token.startswith(delimiter) and not raw_tokens:
            styled_flag = True
            styled_tokens.append(token.lstrip(delimiter))
        elif token.endswith(delimiter):
            styled_tokens.append(token.rstrip(delimiter))
            result_nodes.append(TextNode(" ".join(styled_tokens), text_type))
            styled_tokens.clear()
            styled_flag = False
        elif styled_flag:
            styled_tokens.append(token)
        elif not styled_flag:
            raw_tokens.append(token)

    if raw_tokens:  # catch any leftovers
        result_nodes.append(TextNode(" ".join(raw_tokens), "text"))

    for i, node in enumerate(result_nodes):  # Add spaces where needed
        if node.text_type != "text" and i != 0:
            result_nodes[i - 1].text += " "
        if node.text_type != "text" and i != len(result_nodes) - 1:
            result_nodes[i + 1].text = " " + result_nodes[i + 1].text

    return result_nodes


def extract_markdown_images(text: str) -> list:
    """Takes a Markdown-formatted string with embedded images and returns a list of tuples, where each tuple is of the
    format ("<image alt text>", "<image url>")"""
    result = []

    markdown_image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(markdown_image_pattern, text)
    for match in matches:
        result.append((match[0], match[1]))

    return result


def extract_markdown_links(text: str) -> list:
    """Takes a Markdown-formatted string with embedded images and returns a list of tuples, where each tuple is of the
    format ("<link anchor text>", "<link url>")"""
    result = []

    markdown_link_pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(markdown_link_pattern, text)
    for match in matches:
        result.append((match[0], match[1]))

    return result
