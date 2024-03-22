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


def text_to_textnodes(text: str) -> list:
    node = TextNode(text, "text")
    nodes = split_nodes_delimiter([node], "bold", "**")
    nodes = split_nodes_delimiter(nodes, "italic", "*")
    nodes = split_nodes_delimiter(nodes, "code", "`")
    nodes = split_nodes_image_and_link(nodes)
    nodes = add_spaces_to_appropriate_text_nodes(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            blocks.append(cleaned_block)

    return blocks


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
            new_nodes.extend(create_styled_text_nodes_from_node(node, text_type, delimiter))

    return new_nodes


def split_nodes_image_and_link(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            new_nodes.extend(create_link_and_image_nodes_from_text_node(node))

    return new_nodes


def create_link_and_image_nodes_from_text_node(node: TextNode) -> list:
    string = node.text
    placeholder = "!@#$%^&*()urmom"
    markdown_image_or_link_pattern = r"!?\[.*?\]\(.*?\)"
    matches = re.findall(markdown_image_or_link_pattern, node.text)
    for match in matches:
        string = string.replace(match, placeholder)

    words = []
    result_nodes = []
    current_image_or_link_index = 0
    for token in string.split():
        if token == placeholder and words:
            result_nodes.append(TextNode(" ".join(words), "text"))
            words.clear()

        if token == placeholder:
            markdown_image_or_link = matches[current_image_or_link_index]
            current_image_or_link_index += 1
            result_nodes.append(create_link_or_image_node_from_markdown_link_or_image(markdown_image_or_link))
        else:
            words.append(token)

    if words:  # catch any leftovers
        result_nodes.append(TextNode(" ".join(words), "text"))

    return result_nodes


def create_link_or_image_node_from_markdown_link_or_image(markdown: str) -> TextNode:
    image_or_link = "image" if markdown.startswith("!") else "link"
    pieces = extract_markdown_image_or_link(markdown)
    anchor_or_alt_text = pieces[0]
    url = pieces[1]
    return TextNode(anchor_or_alt_text, image_or_link, url)


def add_spaces_to_appropriate_text_nodes(nodes: list) -> list:
    """Given a list of TextNodes, some of which have a type of "text" and some of which do not, adds a space to all the
    "text" nodes that are adjacent to any non-"text" nodes."""
    for i, node in enumerate(nodes):  # Add spaces where needed
        if node.text_type != "text" and i != 0:
            nodes[i - 1].text += " "
        if node.text_type != "text" and i != len(nodes) - 1:
            nodes[i + 1].text = " " + nodes[i + 1].text

    return nodes


def create_styled_text_nodes_from_node(node: TextNode, text_type: str, delimiter: str) -> list:
    """Transforms a raw TextNode (of text_type of "text") that contains text with valid Markdown syntax for non-nested
    bold, italics, or inline code formatting into a new TextNode of the appropriate type."""
    if node.text.count(delimiter) % 2 != 0:  # Valid markdown must contain an even number of delimiters
        raise Exception(f"Invalid markdown syntax for text: {node.text}")
    if node.text_type != "text":
        return [node]

    result_nodes = []

    text_tokens = []
    for token in node.text.split():
        if token.startswith(delimiter) and token.endswith(delimiter) and text_tokens:
            result_nodes.append(create_text_node(text_tokens, "text"))
            text_tokens.clear()
            result_nodes.append(TextNode(token.lstrip(delimiter).rstrip(delimiter), text_type))
        elif token.startswith(delimiter) and token.endswith(delimiter):
            result_nodes.append(TextNode(token.lstrip(delimiter).rstrip(delimiter), text_type))
        elif token.startswith(delimiter) and text_tokens:
            result_nodes.append(create_text_node(text_tokens, "text"))
            text_tokens.clear()
            text_tokens.append(token.lstrip(delimiter))
        elif token.startswith(delimiter) and not text_tokens:
            text_tokens.append(token.lstrip(delimiter))
        elif token.endswith(delimiter):
            text_tokens.append(token.rstrip(delimiter))
            result_nodes.append(TextNode(" ".join(text_tokens), text_type))
            text_tokens.clear()
        else:
            text_tokens.append(token)

    if text_tokens:  # catch any leftovers
        result_nodes.append(TextNode(" ".join(text_tokens), "text"))

    return result_nodes


def create_text_node(list_of_tokens: list[str], text_type: str) -> TextNode:
    raw_text = " ".join(list_of_tokens)
    return TextNode(raw_text, text_type)


def extract_markdown_image_or_link(text: str) -> tuple:
    """Takes a Markdown-formatted image or link string and returns a string of the format
    ("<image alt text>", "<image url>")"""
    markdown_image_pattern = r"!?\[(.*?)\]\((.*?)\)"
    match = re.findall(markdown_image_pattern, text)[0]
    return match
