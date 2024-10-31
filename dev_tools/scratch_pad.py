import json

a = json.loads('{\n    "water quality": false,\n    "water testing request": false,\n    "product claim": false\n}')

print(type(a))

all_false = not any(a.values())
print(all_false)

{'char_dist': Figure({
    'data': [{'alignmentgroup': 'True',
              'hovertemplate': 'Character=%{x}<br>Frequency=%{y}<extra></extra>',
              'legendgroup': '',
              'marker': {'color': '#000001', 'pattern': {'shape': ''}},
              'name': '',
              'offsetgroup': '',
              'orientation': 'v',
              'showlegend': False,
              'textposition': 'auto',
              'type': 'bar',
              'x': array(['s', ' ', 'i', 't', 'T', 'h', 'a', 'e', '.'], dtype=object),
              'xaxis': 'x',
              'y': array([3, 3, 2, 2, 1, 1, 1, 1, 1], dtype=int64),
              'yaxis': 'y'}],
    'layout': {'barmode': 'relative',
               'legend': {'tracegroupgap': 0},
               'template': '...',
               'title': {'text': 'Character Distribution (Top 20)'},
               'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Character'}},
               'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Frequency'}}}
}), 'entropy_gauge': Figure({
    'data': [{'domain': {'x': [0, 1], 'y': [0, 1]},
              'gauge': {'axis': {'range': [0, 1]},
                        'steps': [{'color': 'lightgray', 'range': [0, 0.7]}, {'color': 'gray', 'range': [0.7, 1]}],
                        'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': 0.7}},
              'mode': 'gauge+number',
              'title': {'text': 'Entropy Ratio'},
              'type': 'indicator',
              'value': 0.3757798660816737}],
    'layout': {'height': 200, 'template': '...'}
}), 'repetition_gauge': Figure({
    'data': [{'domain': {'x': [0, 1], 'y': [0, 1]},
              'gauge': {'axis': {'range': [0, 1]},
                        'steps': [{'color': 'lightgray', 'range': [0, 0.4]}, {'color': 'gray', 'range': [0.4, 1]}],
                        'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': 0.4}},
              'mode': 'gauge+number',
              'title': {'text': 'Repetition Ratio'},
              'type': 'indicator',
              'value': 0.07692307692307687}],
    'layout': {'height': 200, 'template': '...'}
}), 'special chars_gauge': Figure({
    'data': [{'domain': {'x': [0, 1], 'y': [0, 1]},
              'gauge': {'axis': {'range': [0, 1]},
                        'steps': [{'color': 'lightgray', 'range': [0, 0.3]}, {'color': 'gray', 'range': [0.3, 1]}],
                        'threshold': {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': 0.3}},
              'mode': 'gauge+number',
              'title': {'text': 'Special Chars Ratio'},
              'type': 'indicator',
              'value': 0.06666666666666667}],
    'layout': {'height': 200, 'template': '...'}
})}