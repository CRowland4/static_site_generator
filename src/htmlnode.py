class HTMLNode:
    def __init__(self, tag: str = None, props: dict = None, value: str = None, children: list = None):
        if props is None:
            props = {}
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return ",".join([f' {attribute}="{value}"' for attribute, value in self.props.items()])
        else:
            return ""

    def __repr__(self):
        return f"HTMLNODE(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str = None, props: dict = None):
        super().__init__(tag=tag, props=props, value=value)

    def to_html(self):
        if not self.value:
            raise ValueError("Must have a value")
        if not self.tag:
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, children, tag: str = None, props: dict = None):
        super().__init__(children=children, tag=tag, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Must have a value")
        if not self.children:
            raise ValueError("Must have children")

        html = ""
        for child in self.children:
            html += child.to_html()

        return f"<{self.tag}>{html}</{self.tag}>"
