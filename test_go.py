"""Tests for Go engine."""


class TestStone:
    """Test stone placement."""

    def test_color(self):
        """Test allegiance."""
        from src.stone import Stone

    #   Assert intersections are properly hashed.
        assert len(
            {
                Stone(-1, +1, color="white"),
                Stone(+1, -1, color="black"),
                Stone(00, 00),
            }
        ) == 3

    #   Same color means friends even on a different intersection.
        assert Stone(-1, +1, color="white") == Stone(+1, -1, color="white")
        assert Stone(-1, +1, color="black") == Stone(+1, -1, color="black")
        assert Stone(-1, +1, color="empty") == Stone(+1, -1, color="empty")

    #   Different color means foes even on the same intersection.
        assert Stone(00, 00, color="white") != Stone(00, 00, color="black")
        assert Stone(00, 00, color="black") != Stone(00, 00, color="white")

    #   Empty is not friend:
        assert not Stone(00, 00, color="white") == Stone(00, 00, color="empty")
        assert not Stone(00, 00, color="black") == Stone(00, 00, color="empty")
        assert not Stone(00, 00, color="empty") == Stone(00, 00, color="white")
        assert not Stone(00, 00, color="empty") == Stone(00, 00, color="black")

    #   Empty is not foe:
        assert not Stone(00, 00, color="white") != Stone(00, 00, color="empty")
        assert not Stone(00, 00, color="black") != Stone(00, 00, color="empty")
        assert not Stone(00, 00, color="empty") != Stone(00, 00, color="white")
        assert not Stone(00, 00, color="empty") != Stone(00, 00, color="black")


class TestIntersection:
    """Test intersection operations."""

    def test_init(self):
        """Test proper generation of intersections."""
        from src.intersection import Intersection

    #   Assert size does stay positive.
        assert Intersection(0, 0, -9).size == 9

    #   Boundary checks inside board limits.
        assert Intersection(-1, +1, 1)

    #   Boundary checks outside board limits.
        assert not Intersection(-2, +1, 1)
        assert not Intersection(-1, +2, 1)

    def test_operations(self):
        """Test intersection vector operations."""
        from src.intersection import Intersection

    #   Binary operations:
        assert Intersection(-1, +2, 0) + Intersection(-3, +4, 0) == Intersection(-4, +6, 0)
        assert Intersection(-1, +2, 0) - Intersection(-3, +4, 0) == Intersection(+2, -2, 0)

    #   Multiplication:
        assert Intersection(-1, +2, 0) * 2 == Intersection(-2, +4, 0)
        assert 2 * Intersection(-3, +4, 0) == Intersection(-6, +8, 0)

    #   Unary operations:
        assert +Intersection(-1, +2, 0) == Intersection(-1, +2, 0)
        assert -Intersection(-3, +4, 0) == Intersection(+3, -4, 0)


class TestUndirected:
    """Test (undirected) Graph objects."""

    def test_init(self):
        """Test graph creation."""
        from src.graph import Neighborhood, Undirected

        graph = Undirected.fromkeys(
            {
                1,
                2,
                3,
            }
        )

    #   Assert graph with isolated nodes is built.
        for node in graph:
            assert graph[node] == Neighborhood()

    #   Graph will be empty after clearing, as no pair of nodes is connected.
        graph.clear()
        assert graph == Undirected()

    #   Graph should be reproducible from its own edgelist.
        assert graph == Undirected.from_edge_list(graph.edge_list)

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

    #   Popping should be using deletion.
        assert graph.pop(4, {1, 2, 3}) == {1, 2, 3}  # 4 is no longer a node so return the default given.
        assert graph.pop(3) == {1}  # pop returns the popped value
        assert 3 not in graph
        assert 3 not in graph[1]  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.

    #   Popping item should be using pop?
        assert graph.popitem() == (2, {1})  # popitems returns the popped items (key and value)
        assert 2 not in graph[1]  # The symmetric edge should be missing too. NOTE: It does not, because it is written in C.

    #   Clear isolated nodes.
        graph.clear()
        assert graph == Undirected()

    def test_special(self):
        """Test methods related to clustering and edge listing."""
        from src.graph import Clusters, Edges, Neighborhood, Nodes, Undirected

        graph = Undirected(
            {
                1: {
                    2,
                    3,
                    4,
                },
                5: {
                    6,
                    7,
                },
                8: {
                    9,
                },
                0: Neighborhood()
            }
        )

    #   Assert disconnected nodes are allowed.
        assert graph[0] == Neighborhood()

    #   Assert clusters are as indicated by the directed initialization of this undirected graph.
        assert graph.clusters == Clusters(
            {
                Nodes(
                    {
                        1,
                        2,
                        3,
                        4,
                    }
                ),
                Nodes(
                    {
                        5,
                        6,
                        7,
                    }
                ),
                Nodes(
                    {
                        8,
                        9,
                    }
                ),
                Nodes(
                    {
                        0,
                    }
                ),
            }
        )

    #   Assert nodes belong to their clusters.
        for node in graph:
            assert node in graph.cluster(node)

    #   Check edgelist.
        assert graph.edge_list == Edges(
            {
                (1, 2), (2, 1),
                (1, 3), (3, 1),
                (1, 4), (4, 1),
                (5, 6), (6, 5),
                (5, 7), (7, 5),
                (8, 9), (9, 8),
            }
        )

    #   Check edgelist is the same even after clearing isolated nodes.
        graph.clear()
        assert 0 not in graph
        assert graph.edge_list == Edges(
            {
                (1, 2), (2, 1),
                (1, 3), (3, 1),
                (1, 4), (4, 1),
                (5, 6), (6, 5),
                (5, 7), (7, 5),
                (8, 9), (9, 8),
            }
        )
