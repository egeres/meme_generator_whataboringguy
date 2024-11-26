import numpy as np
import plotly.graph_objects as go


def plot_points_in_unit_circle(points: list[tuple[float, float]]):
    """
    Plots the given points within a unit circle using Plotly.

    Parameters:
    points (list[tuple[float, float]]): List of (x, y) tuples to plot.
    """
    # Unzip the list of tuples into x and y coordinates
    x, y = zip(*points)

    # Create a scatter plot of the points
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(size=5, color="blue"),
            name="Random Points",
        )
    )

    # Add a circle representing the unit circle boundary
    circle_theta = np.linspace(0, 2 * np.pi, 500)
    circle_x = np.cos(circle_theta)
    circle_y = np.sin(circle_theta)
    fig.add_trace(
        go.Scatter(
            x=circle_x,
            y=circle_y,
            mode="lines",
            line=dict(color="red"),
            name="Unit Circle",
        )
    )

    # Set the aspect ratio to 1:1 to make the circle look circular
    fig.update_layout(
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(constrain="domain"),
        title="Random Points Within a Unit Circle",
        showlegend=False,
    )

    # Show the plot
    fig.show()


if __name__ == "__main__":
    from meme_generator_whataboringguy.point_generator import foo_random

    N = 200
    points = foo_random(N, 0.7 / np.sqrt(N))
    plot_points_in_unit_circle(points)
