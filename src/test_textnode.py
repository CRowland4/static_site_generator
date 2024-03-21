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
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
                  ]
        self.assertEqual(textnode.create_styled_nodes_from_node(node, "code", "`"), result)
        return

    def test_extract_markdown_images(self):
        text = ("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another]("
                "https://i.imgur.com/dfsdkjfd.png)")
        result = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        self.assertEqual(textnode.extract_markdown_images(text), result)
        return

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(textnode.extract_markdown_links(text), result)
        return


if __name__ == '__main__':
    unittest.main()
