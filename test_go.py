"""Tests for Go engine."""


from unittest import TestCase


class TestUndirected(TestCase):
    """Test Graph objects."""

    def test_init(self):
        """Test graph creation."""
        from src.graph import Undirected

        graph = Undirected.fromkeys(
            {
                1,
                2,
                3,
            }
        )

    def test_set(self):
        """Test setting and updating methods."""
        from src.graph import Neighborhood, Undirected

        graph = Undirected(
            {
                1: {
                    1,  # self-reference
                    2,  # includes symmetric
                },
                2: {
                    1,  # includes symmetric
                    4,  # misses symmetric with node missing
                },
                3: {
                    1,  # misses symmetric but node included
                    3,  # self-reference
                },
            }
        )
        should_be = {
            1: {
                2,
                3,
            },
            2: {
                1,
                4,
            },
            3: {
                1,
            },
            4: {
                2,
            }
        }

    #   Test undirected graph creation which fills missing symmetric edges.
        assert graph == should_be

    #   Test if other methods for altering the graph are affected by the symmetric setter.
        graph.update({1: {5}})  # Try and update graph. This also tests adding.
        should_be.update({1: should_be[1] | {5}, 5: {1}})  # The graph should contain both edge directions.
        assert graph == should_be
        assert graph.setdefault(1, {4}) == {
            2,
            3,
            5,  # Added just before.
        }  # Node 1 exists, so get its proper neighborhood.
        assert graph.setdefault(6, {4}) == {4}  # Node 6 does not exist, so set the default {4}.
        assert graph.setdefault(7) == Neighborhood()  # Node 7 does not exist, so set the default empty set.

    def test_get(self):
        """Test getting methods."""
        from src.graph import Undirected

        graph = Undirected(
            {
                1: {
                    1,  # self-reference
                    2,  # includes symmetric
                },
                2: {
                    1,  # includes symmetric
                    4,  # misses symmetric with node missing
                },
                3: {
                    1,  # misses symmetric but node included
                    3,  # self-reference
                },
            }
        )

    #   Test how normal key access returns neighborhoods.
        assert graph[1] == {
            2,
            3,
        }
        assert 1 in graph[2]
        assert 1 in graph[3]

    #   Test how the `get` method with default value works.
        assert graph.get(1, {4}) == {
            2,
            3,
        }  # Node 1 exists, so get its proper neighborhood.
        assert graph.get(5, {4}) == {4}  # Node 5 does not exist, so get the default {4}.

    def test_del(self):
        """Test deleting methods."""
        from src.graph import Undirected

        graph = Undirected(
            {
                1: {
                    2,
                    3,
                },
                2: {
                    1,
                    4,
                },
                3: {
                    1,
                },
                4: {
                    2,
                }
            }
        )

    #   Plain-delete node 4 and connected edges.
        del graph[4]
        assert 4 not in graph
        assert 4 not in graph[2]  # The symmetric edge should be missing too.

    #   Popping should be using deletion:
        assert graph.pop(4, {1, 2, 3}) == {1, 2, 3}  # 4 is no longer a node so return the default given.
        assert graph.pop(3) == {1}  # pop returns the popped value
        assert 3 not in graph
        assert 3 not in graph[1]  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.

    #   Popping item should be using pop?
        assert graph.popitem() == (2, {1})  # popitems returns the popped items (key and value)
        assert graph == {}  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.
