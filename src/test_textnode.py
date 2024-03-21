import unittest
import textnode

from textnode import TextNode


class TextNodeTest(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a text node", "bold", "url.com")
        node4 = TextNode("This is a text node", "bold", "url.com")
        node5 = TextNode("This is a text node", "italics")
        node6 = TextNode("This is a DIFFERENT text node", "bold")
        self.assertEqual(node1, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertNotEqual(node5, node6)
        return

    def test_create_styled_nodes_from_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        result = [
            TextNode("This is text with a", "text"),
            TextNode("code block", "code"),
            TextNode("word", "text")
        ]
        self.assertEqual(textnode.create_styled_text_nodes_from_node(node, "code", "`"), result)
        return

    def test_extract_markdown_image_or_link(self):
        image_text = "![another](https://i.imgur.com/dfsdkjfd.png)"
        result = ("another", "https://i.imgur.com/dfsdkjfd.png")
        self.assertEqual(textnode.extract_markdown_image_or_link(image_text), result)

        link_text = "[another](https://www.example.com/another)"
        result = ("another", "https://www.example.com/another")
        self.assertEqual(textnode.extract_markdown_image_or_link(link_text), result)
        return

    def test_create_link_or_image_nodes_from_text_node(self):
        test = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            "text",
        )
        result = [
            TextNode("This is text with an", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("and another", "text"),
            TextNode(
                "second image", "image", "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(result, textnode.create_link_and_image_nodes_from_text_node(test))
        return

    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(result, textnode.text_to_textnodes(text))
        return


if __name__ == '__main__':
    unittest.main()
