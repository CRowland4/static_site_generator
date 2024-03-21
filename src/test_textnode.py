import unittest

from textnode import TextNode, create_styled_nodes_from_node


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
        self.assertNotEquals(node1, node3)
        self.assertNotEquals(node1, node4)
        self.assertNotEquals(node5, node6)
        return

    def test_create_styled_nodes_from_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        result = [TextNode(text="This is text with a ", text_type="text", url=""), TextNode(text="code block", text_type="code", url=""), TextNode(text=" word", text_type="text", url="")]
        self.assertEqual(create_styled_nodes_from_node(node, "code", "`"), result)
        return


if __name__ == '__main__':
    unittest.main()
