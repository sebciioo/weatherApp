import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

"""
    Generowanie wykresu na stronie z historycznymi danymi dla danego miasta
"""


def generate_chart(dates, values, parameter, city):
    plt.figure(figsize=(10, 5), facecolor='none')

    df = pd.DataFrame({'date': dates, 'value': values})
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
    df = df.sort_values('date')

    """Style"""
    plt.plot(df['date'], df['value'], marker='o', color='white')
    plt.title(f'{parameter.capitalize()} in {city}', color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel(parameter.capitalize(), color='white')
    plt.grid(True, color='gray', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    ax = plt.gca()
    ax.patch.set_alpha(0)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.subplots_adjust(bottom=0.25)

    """Zapisywanie do pliku"""
    chart_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'chart')
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, 'chart.png')
    plt.savefig(chart_path, transparent=True)
    plt.close()

    return chart_path


