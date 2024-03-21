import unittest

from htmlnode import ParentNode, LeafNode


class ParentNodeTest(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", ""),
                LeafNode("italic text", "i"),
                LeafNode("Normal text", ""),
            ],
            "p",
        )
        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), result)
        return


if __name__ == "__main__":
    unittest.main()
