import numpy as np
import plotly.graph_objects as go

# Paramètres de base
E = 0.1E9          # Module de Young du caoutchouc [Pa]
N = 25200          # Nombre total de câbles qui s'enroulent
e = 5.0E-2         # Diamètre de l'élastique [mètre]

# Constante de conversion en MWh
Constante = (2.778E-10 * np.pi**3) / 2

# Fonction de calcul de l'énergie
def f(n, r, l0):
    return (Constante * E * (n**2) * (e**2) * (r + e * (n - 1) / 2)**2) / l0

# Discrétisation des axes
n = np.linspace(1, 30, 100)         # Nombre de tours
r = np.linspace(0., 1, 100)         # Rayon de l'enrouleur [mètre]
X, Y = np.meshgrid(n, r)

# Liste des valeurs de l0 pour le slider
l0_values = np.linspace(3, 200, 50)  # 50 valeurs entre 3 et 200

# Génération des surfaces pour chaque valeur de l0
frames = []
for l0 in l0_values:
    Z = f(X, Y, l0)
    frame = go.Frame(
        data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')],
        name=f"{l0:.1f}"  # Le nom correspond à la valeur de l0
    )
    frames.append(frame)

# Surface initiale pour l0 = 50
Z_initial = f(X, Y, l0_values[0])
surface = go.Surface(z=Z_initial, x=X, y=Y, colorscale='Viridis')

# Création du graphique avec slider
fig = go.Figure(
    data=[surface],
    layout=go.Layout(
        title="3D Plot with Adjustable l0",
        scene=dict(
            xaxis_title="Nombre de tours (n)",
            yaxis_title="Rayon de l'enrouleur (r)",
            zaxis_title="Énergie stockable [MWh]",
        ),
        width=1000,
        height=800,
        sliders=[{
            "steps": [
                {
                    "args": [[f"{l0:.1f}"], {"frame": {"duration": 50, "redraw": True}}],
                    "label": f"{l0:.1f}",
                    "method": "animate",
                }
                for l0 in l0_values
            ],
            "currentvalue": {
                "prefix": "l0 = ",
                "visible": True,
                "font": {"size": 20}
            },
        }],
    ),
    frames=frames
)

# Ajout d'une animation pour interagir avec le slider
fig.update_layout(updatemenus=[
    {
        "type": "buttons",
        "showactive": False,
        "buttons": [
            {
                "label": "▶️ Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
            },
            {
                "label": "⏸️ Pause",
                "method": "animate",
                "args": [[None], {"frame": {"duration": 0, "redraw": False}}],
            }
        ],
    }
])

fig.show()
