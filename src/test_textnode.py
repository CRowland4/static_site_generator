import unittest

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
        self.assertNotEquals(node1, node3)
        self.assertNotEquals(node1, node4)
        self.assertNotEquals(node5, node6)
        return


if __name__ == '__main__':
    unittest.main()
