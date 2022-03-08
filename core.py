from typing import List, Tuple, Optional, Dict
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import picture, plotting, thermal


class ThermalImage:
    _image: np.ndarray
    _temperatures: np.ndarray
    _uncertainties: np.ndarray
    _lines: List[np.ndarray]
    _rects: List[np.ndarray]

    def __init__(self, image: np.ndarray, temperatures: np.ndarray, uncertainties: Optional[np.ndarray] = None):
        if uncertainties is None:
            uncertainties = np.zeros_like(temperatures)
        self._image = image
        self._temperatures = temperatures
        self._uncertainties = uncertainties
        self._lines, self._rects = [], []

    def plot_image(self):
        plotting.plot_image(self._image)
    
    def plot_temperatures(self):
        plotting.plot_image(self._temperatures)

    def add_line(self, x1: int, y1: int, x2: int, y2: int):
        line_points = np.array([[x1, y1], [x2, y2]])
        self._lines.append(line_points)
    
    def add_rectangle(self, x1: int, y1: int, x2: int, y2: int):
        rect_points = np.array([[x1, y1], [x2, y2]])
        self._rects.append(rect_points)

    def plot_selection(self):
        line_coords = [picture._get_line_coords(l) for l in self._lines]
        rect_coords = [picture._get_rect_coords(r) for r in self._rects]
        plotting.plot_image(self._temperatures, line_coords=line_coords, rect_coords=rect_coords)
        for line in self._lines:
            x_line, y_line, z_line = picture.select_line(self._temperatures, line)
            tolerance = thermal.get_line_uncertainty(self._uncertainties, x_line, y_line)
            plotting.plot_line(z_line, tolerance)

        for rect in self._rects:
            rect_select = picture.select_rectangle(self._temperatures, rect)
            plotting.plot_image(rect_select)
            plotting.plot_histogram(rect_select)
