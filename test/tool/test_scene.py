import unittest
from test import fake_const as fc


class Scene:
    @classmethod
    def is_long_name(cls, node: str) -> bool:
        return True if node.startswith("|") else False

    @classmethod
    def is_shape(cls, node: str) -> bool:
        return True if node.endswith("Shape") else False

    @classmethod
    def get_short_name(cls, node: str) -> str:
        return node.split("|")[-1]

    @classmethod
    def get_transform(cls, node: str) -> str:
        if not cls.is_shape(node):
            return node
        if not cls.is_long_name(node):
            return node.split("Shape")[0]
        return "|".join(node.split("|")[:-1])

    @classmethod
    def get_shape(cls, node: str) -> str:
        return node if cls.is_shape(node) else f"{node}Shape"

    @classmethod
    def get_unique_short_names(cls, nodes: list) -> list:
        seen = set()
        return [
            seen.add(cls.get_short_name(n)) or cls.get_short_name(n)
            for n in nodes
            if cls.get_short_name(n) not in seen
        ]

    @classmethod
    def get_transform_nodes(cls, nodes: list):
        seen = set()
        return [
            seen.add(cls.get_transform(n)) or cls.get_transform(n)
            for n in nodes
            if cls.get_transform(n) not in seen
        ]


class SceneTest(unittest.TestCase):
    def test_long_name_node_with_is_long_name(self):
        # "|Camera_13" -> True
        node = "|Camera_13"
        actual = Scene.is_long_name(node)
        self.assertEqual(actual, True)

    def test_short_name_node_with_is_long_name(self):
        # "Camera_13" -> False
        node = "Camera_13"
        actual = Scene.is_long_name(node)
        self.assertEqual(actual, False)

    def test_long_name_node_with_get_short_name(self):
        # "|Camera_13" -> "Camera_13"
        node = "|Camera_13|Camera_13Shape"
        actual = Scene.get_short_name(node)
        self.assertEqual(actual, "Camera_13Shape")

    def test_short_name_node_with_get_short_name(self):
        # "Camera_13" -> "Camera_13"
        node = "Camera_13"
        actual = Scene.get_short_name(node)
        self.assertEqual(actual, "Camera_13")

    def test_long_name_transform_node_with_get_transform(self):
        # "|Camera_13" -> "|Camera_13"
        node = "|Camera_13"
        actual = Scene.get_transform(node)
        self.assertEqual(actual, "|Camera_13")

    def test_short_name_transform_node_with_get_transform(self):
        # "Camera_13" -> "Camera_13"
        node = "Camera_13"
        actual = Scene.get_transform(node)
        self.assertEqual(actual, "Camera_13")

    def test_long_name_shape_node_with_get_transform(self):
        # "|Camera_13|Camera_13Shape" -> "|Camera_13"
        node = "|Camera_13|Camera_13Shape"
        actual = Scene.get_transform(node)
        self.assertEqual(actual, "|Camera_13")

    def test_short_name_shape_node_with_get_transform(self):
        # "Camera_13Shape" -> "Camera_13"
        node = "Camera_13Shape"
        actual = Scene.get_transform(node)
        self.assertEqual(actual, "Camera_13")

    def test_long_name_transform_node_with_get_shape(self):
        # "|Camera_13" -> "|Camera_13Shape"
        node = "|Camera_13"
        actual = Scene.get_shape(node)
        self.assertEqual(actual, "|Camera_13Shape")

    def test_short_name_transform_node_with_get_shape(self):
        # "Camera_13" -> "Camera_13Shape"
        node = "Camera_13"
        actual = Scene.get_shape(node)
        self.assertEqual(actual, "Camera_13Shape")

    def test_long_name_shape_node_with_get_shape(self):
        # "|Camera_13|Camera_13Shape" -> "|Camera_13|Camera_13Shape"
        node = "|Camera_13|Camera_13Shape"
        actual = Scene.get_shape(node)
        self.assertEqual(actual, "|Camera_13|Camera_13Shape")

    def test_short_name_shape_node_with_get_shape(self):
        # "Camera_13Shape" -> "Camera_13Shape"
        node = "Camera_13Shape"
        actual = Scene.get_shape(node)
        self.assertEqual(actual, "Camera_13Shape")


if __name__ == "__main__":
    unittest.main()
