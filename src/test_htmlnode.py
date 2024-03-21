import unittest

from htmlnode import HTMLNode, LeafNode


class HTMLNodeTest(unittest.TestCase):
    @staticmethod
    def test_props_to_html():
        node1 = HTMLNode()
        assert node1.props_to_html() == ""

        node2 = HTMLNode(props={"foo": "bar", "bar": "baz"})
        assert node2.props_to_html() == ' foo="bar", bar="baz"'


if __name__ == '__main__':
    unittest.main()
