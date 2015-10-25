# -*- coding: utf-8 -*-

"""Test interact."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from itertools import product

import numpy as np
from vispy.util import keys

from ..base import BaseVisual
from ..interact import Grid, Boxed, Stacked
from ..panzoom import PanZoom
from ..transform import NDC


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

class MyTestVisual(BaseVisual):
    vertex = """
        attribute vec2 a_position;
        void main() {
            gl_Position = transform(a_position);
            gl_PointSize = 2.;
        }
        """
    fragment = """
        void main() {
            gl_FragColor = vec4(1, 1, 1, 1);
        }
    """
    gl_primitive_type = 'points'

    def get_shaders(self):
        return self.vertex, self.fragment

    def set_data(self):
        n = 1000

        coeff = [(1 + i + j) for i, j in product(range(2), range(3))]
        coeff = np.repeat(coeff, n)
        coeff = coeff[:, None]

        position = .1 * coeff * np.random.randn(2 * 3 * n, 2)

        self.program['a_position'] = position.astype(np.float32)


def _create_visual(qtbot, canvas, interact, box_index):
    c = canvas

    # Attach the interact *and* PanZoom. The order matters!
    interact.attach(c)
    PanZoom(aspect=None, constrain_bounds=NDC).attach(c)

    visual = MyTestVisual()
    visual.attach(c)
    visual.set_data()

    visual.program['a_box_index'] = box_index.astype(np.float32)

    c.show()
    qtbot.waitForWindowShown(c.native)


#------------------------------------------------------------------------------
# Test grid
#------------------------------------------------------------------------------

def test_grid_1(qtbot, canvas):

    c = canvas
    n = 1000

    box_index = [[i, j] for i, j in product(range(2), range(3))]
    box_index = np.repeat(box_index, n, axis=0)

    grid = Grid(2, 3)
    _create_visual(qtbot, canvas, grid, box_index)

    # No effect without modifiers.
    c.events.key_press(key=keys.Key('+'))
    assert grid.zoom == 1.

    # Zoom with the keyboard.
    c.events.key_press(key=keys.Key('+'), modifiers=(keys.CONTROL,))
    assert grid.zoom > 1

    # Unzoom with the keyboard.
    c.events.key_press(key=keys.Key('-'), modifiers=(keys.CONTROL,))
    assert grid.zoom == 1.

    # Set the zoom explicitly.
    grid.zoom = 2
    assert grid.zoom == 2.

    # Press 'R'.
    c.events.key_press(key=keys.Key('r'))
    assert grid.zoom == 1.

    # qtbot.stop()


def test_boxed_1(qtbot, canvas):

    n = 6
    b = np.zeros((n, 4))

    b[:, 0] = b[:, 1] = np.linspace(-1., 1. - 1. / 3., n)
    b[:, 2] = b[:, 3] = np.linspace(-1. + 1. / 3., 1., n)

    n = 1000
    box_index = np.repeat(np.arange(6), n, axis=0)

    boxed = Boxed(box_bounds=b)
    _create_visual(qtbot, canvas, boxed, box_index)

    # qtbot.stop()


def test_stacked_1(qtbot, canvas):

    n = 1000
    box_index = np.repeat(np.arange(6), n, axis=0)

    stacked = Stacked(n_boxes=6, margin=-10)
    _create_visual(qtbot, canvas, stacked, box_index)

    # qtbot.stop()
