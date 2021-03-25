import plotly.graph_objects as go

import numpy as np

# Generate curve data
N = 100
t = np.linspace(1, 100, N)  # static line plot
x = t
y = t**2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 150
yM = np.max(y) + 150


# fig data

# fig layout
layout_xaxis = dict(range=[xm, xM], autorange=False, zeroline=False)
layout_yaxis = dict(range=[ym, yM], autorange=False, zeroline=False)
layout_updatemenus = [dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]

# Create figure
fig = go.Figure(
    layout=go.Layout(
        xaxis=layout_xaxis,
        yaxis=layout_yaxis,
        title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
        updatemenus=layout_updatemenus),

)

for step in np.linspace(1, 100, N):  # generate traces for animated point
    x_step = (step,)
    y_step = (step**2,)
    fig.add_trace(
        go.Scatter(
            visible=False,
            mode="markers",
            marker=dict(color="red", size=10),
            x=x_step,
            y=y_step
        )
    )

fig.data[0].visible = True


fig.add_trace(  # line plot
    go.Scatter(
        mode="lines",
        visible=True,
        marker=dict(color="blue"),
        x=x,
        y=y
    )
)


# set slider steps
steps = []

for i in range(N):  # set point to visible
    step = dict(
        method="update",
        args=[{"visible": ([False] * N) +
                          ([True] * (len(fig.data) - N))}],
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)


sliders = [dict(
    active=0,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]


fig.update_layout(
    sliders=sliders
)


fig.show()
