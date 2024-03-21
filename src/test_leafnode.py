import unittest

from htmlnode import LeafNode


class LeafNodeTest(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode("This is a paragraph of text.", "p")
        node1_result = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node1.to_html(), node1_result)

        node2 = LeafNode("Click me!", "a", {"href": "https://www.google.com"}, )
        node2_result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node2.to_html(), node2_result)

        node3 = LeafNode("", "p", {"color": "red"})
        self.assertRaises(ValueError, node3.to_html)
        return


if __name__ == '__main__':
    unittest.main()
