import networkx as nx
from plotly.graph_objs import Scatter, Figure
import graph
import plotly.graph_objects as go
COLOUR_SCHEME = [
    '#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A', '#B68100',
    '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    '#6C7C32', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    '#6C4516', '#0D2A63', '#AF0038'
]

LINE_COLOUR = 'rgb(66,79,70)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
BOOK_COLOUR = 'rgb(89, 205, 105)'
USER_COLOUR = 'rgb(105, 89, 205)'
h5_COLOUR = 'rgb(255, 217, 102)'
red_COLOUR= 'rgb(220,20,60)'

def visualize_graph(graph: graph.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 50000,
                    output_file: str = '',item=None,title='') -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    names = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]
    colours = []
    for name in names:
        if name==item:
            colours.append(red_COLOUR)
        elif name[-1] == '1':
            colours.append(BOOK_COLOUR)
        elif name[-1] == '3':
            colours.append(USER_COLOUR)
        else:
            colours.append(h5_COLOUR)
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=3),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=10 - max_vertices // 2000,
                                 color=colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout(title_text=title, showlegend=False,margin=dict(l=50, r=50, t=50, b=50))
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


def visualize_directedgraph(graph: graph.Graph,
                            layout: str = 'spring_layout',
                            max_vertices: int = 50000,
                            output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given graph.

        Optional arguments:
            - layout: which graph layout algorithm to use
            - max_vertices: the maximum number of vertices that can appear in the graph
            - output_file: a filename to save the plotly image to (rather than displaying
                in your web browser)
        """
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    names = [graph_nx.nodes[k]['kind'][-1] for k in graph_nx.nodes]
    colours = []
    for name in names:
        if name == '1':
            colours.append(BOOK_COLOUR)
        elif name == '3':
            colours.append(USER_COLOUR)
        else:
            colours.append(h5_COLOUR)
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = go.Scatter(
        x=x_edges,
        y=y_edges,
        mode='lines+markers+text',  # Add 'markers' to show arrows
        name='edges',
        line=dict(color=LINE_COLOUR, width=5),
        marker=dict(symbol='arrow', size=10),  # Define arrow symbol and size
        hoverinfo='none',
    )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)



