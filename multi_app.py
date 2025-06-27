import pandas as pd
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from flask import render_template_string


# Cargar los datos
file_id = "1PWTw-akWr59Gu7MoHra5WXMKwllxK9bp"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
df = pd.read_csv(url)

# Clasificación por edad
def clasificar_edad(edad):
    if edad < 13:
        return "Niño"
    elif edad < 19:
        return "Adolescente"
    elif edad < 30:
        return "Joven"
    elif edad < 61:
        return "Adulto"
    elif edad < 200:
        return "Adulto mayor"

df['Rango de Edad'] = df['EDAD'].apply(clasificar_edad)

# Clasificación por días de espera
def clasificar_dias(dias):
    if dias < 10:
        return "0-9"
    elif dias < 20:
        return "10-19"
    elif dias < 30:
        return "20-29"
    elif dias < 40:
        return "30-39"
    elif dias < 50:
        return "40-49"
    elif dias < 60:
        return "50-59"
    elif dias < 70:
        return "60-69"
    elif dias < 80:
        return "70-79"
    elif dias < 90:
        return "80-89"
    else:
        return "90+"

df['RANGO_DIAS'] = df['DIFERENCIA_DIAS'].apply(clasificar_dias)

# Crear servidor Flask compartido
server = Flask(__name__)

# Ruta raíz
@server.route('/')
def index():
    return render_template_string("""
    <html>
    <head>
        <title>Bienvenido</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                text-align: center;
                padding: 50px;
                color: #333;
            }
            h2 {
                color: #2c3e50;
            }
            .logo {
                width: 80px;
                height: auto;
                margin-bottom: 20px;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                display: inline-block;
                max-width: 600px;
                width: 100%;
                animation: fadeIn 1s ease-in-out;
                box-sizing: border-box;
            }
            .links {
                margin-top: 30px;
            }
            a {
                display: inline-block;
                margin: 10px;
                margin-bottom: 15px;
                padding: 12px 24px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease, transform 0.2s ease;
                box-sizing: border-box;
            }
            a:hover {
                background-color: #2980b9;
                transform: scale(1.05);
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* --- Media Queries para responsividad --- */
            @media (max-width: 768px) {
                body {
                    padding: 20px;
                }
                .container {
                    padding: 20px;
                    margin: 0 auto;
                    max-width: 95%;
                }
                h2 {
                    font-size: 1.8em;
                }
                .logo {
                    width: 70px;
                }
                a {
                    display: block;
                    width: calc(100% - 20px);
                    margin: 10px auto;
                    padding: 10px 15px;
                    font-size: 1em;
                }
            }

            @media (max-width: 480px) {
                body {
                    padding: 10px;
                }
                .container {
                    padding: 15px;
                }
                h2 {
                    font-size: 1.5em;
                }
                .logo {
                    width: 50px;
                }
                a {
                    font-size: 0.9em;
                    padding: 8px 12px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.png" alt="Logo de la Institución" class="logo">
            <h2>Bienvenido</h2>
            <p>Explora las siguientes visualizaciones:</p>
            <div class="links">
                <a href="/edad/">Distribución por Edad</a>
                <a href="/espera/">Tiempos de Espera</a>
                <a href="/modalidad/">Modalidad de Atención</a>
                <a href="/asegurados/">Estado del Seguro</a>
                <a href="/tiempo/">Línea de Tiempo</a>
            </div>
        </div>
    </body>
    </html>
    """)


# App 1: Por Rango de Edad (ACTUALIZADA con 3 PIES)
app_edad = dash.Dash(__name__, server=server, url_base_pathname='/edad/')
app_edad.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Distribución por Rango de Edad", style={'textAlign': 'center'}),
    dcc.Graph(id='histogram-edad', figure=px.histogram(
        df,
        x='Rango de Edad',
        category_orders={'Rango de Edad': ["Niño", "Adolescente", "Joven", "Adulto", "Adulto mayor"]},
        title='Distribución de edades de los pacientes del hospital María Auxiliadora',
        labels={'Rango de Edad': 'Rango de Edad'},
        template='plotly_white'
    )),
    html.Div([ # Contenedor para los tres gráficos de pastel dependientes para responsividad
        html.Div([
            dcc.Graph(id='pie-chart-edad-especialidades', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}),

        html.Div([
            dcc.Graph(id='pie-chart-edad-sexo', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}),

        html.Div([
            dcc.Graph(id='pie-chart-edad-seguro', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
])

@app_edad.callback(
    [Output('pie-chart-edad-especialidades', 'figure'),
     Output('pie-chart-edad-sexo', 'figure'),
     Output('pie-chart-edad-seguro', 'figure')],
    Input('histogram-edad', 'clickData')
)
def update_edad_charts(clickData):
    # Valores iniciales si no hay clic o para reiniciar los gráficos
    empty_pie_especialidades = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)
    empty_pie_sexo = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)
    empty_pie_seguro = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)

    if clickData is None:
        return empty_pie_especialidades, empty_pie_sexo, empty_pie_seguro

    selected_range = clickData['points'][0]['x']
    filtered_df = df[df['Rango de Edad'] == selected_range].copy()

    # --- 1. Gráfico de Pastel de Especialidades (Top 5) ---
    top_especialidades = filtered_df['ESPECIALIDAD'].value_counts().nlargest(5)
    filtered_df['ESPECIALIDAD_AGRUPADA'] = filtered_df['ESPECIALIDAD'].apply(
        lambda x: x if x in top_especialidades.index else 'Otras'
    )
    grouped_especialidades = filtered_df['ESPECIALIDAD_AGRUPADA'].value_counts().reset_index()
    grouped_especialidades.columns = ['ESPECIALIDAD', 'CUENTA']
    fig_especialidades = px.pie(
        grouped_especialidades,
        names='ESPECIALIDAD',
        values='CUENTA',
        title=f"Top 5 Especialidades para el rango de edad '{selected_range}'",
        height=500
    )
    fig_especialidades.update_traces(textposition='inside', textinfo='percent+label')
    fig_especialidades.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # --- 2. Gráfico de Pastel de Distribución por Sexo ---
    sexo_counts = filtered_df['SEXO'].value_counts().reset_index()
    sexo_counts.columns = ['SEXO', 'CUENTA']
    fig_sexo = px.pie(
        sexo_counts,
        names='SEXO',
        values='CUENTA',
        title=f"Distribución de Sexo para el rango de edad '{selected_range}'",
        height=500
    )
    fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
    fig_sexo.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # --- 3. Gráfico de Pastel de Distribución por Estado de Seguro ---
    # Asegúrate de manejar los valores NaN si existen en la columna 'SEGURO'
    seguro_counts = filtered_df['SEGURO'].value_counts().reset_index()
    seguro_counts.columns = ['SEGURO', 'CUENTA']
    fig_seguro = px.pie(
        seguro_counts,
        names='SEGURO',
        values='CUENTA',
        title=f"Distribución de Seguro para el rango de edad '{selected_range}'",
        height=500
    )
    fig_seguro.update_traces(textposition='inside', textinfo='percent+label')
    fig_seguro.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return fig_especialidades, fig_sexo, fig_seguro


# App 2: Por Rango de Días de Espera
app_espera = dash.Dash(__name__, server=server, url_base_pathname='/espera/')
app_espera.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Distribución por Tiempo de Espera", style={'textAlign': 'center'}),
    dcc.Graph(id='histogram-espera', figure=px.histogram(
        df,
        x='RANGO_DIAS',
        category_orders={'RANGO_DIAS': ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"]},
        title='Distribución de la Cantidad de Pacientes según su Tiempo de Espera',
        labels={'RANGO_DIAS': 'Rango de Días'},
        template='plotly_white'
    )),
    html.Div([ # Contenedor para los tres gráficos de pastel dependientes para responsividad
        html.Div([
            dcc.Graph(id='pie-chart-espera-especialidades', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}), # max-width para 2 por fila

        html.Div([
            dcc.Graph(id='pie-chart-espera-sexo', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}), # max-width para 2 por fila

        html.Div([
            dcc.Graph(id='pie-chart-espera-atendido', figure=px.pie(
                names=[], values=[], title="Seleccione una barra en el histograma", height=400
            ))
        ], style={'width': '100%', 'max-width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}) # max-width para 2 por fila
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
])

@app_espera.callback(
    [Output('pie-chart-espera-especialidades', 'figure'),
     Output('pie-chart-espera-sexo', 'figure'),
     Output('pie-chart-espera-atendido', 'figure')],
    Input('histogram-espera', 'clickData')
)
def update_espera_charts(clickData):
    # Valores iniciales si no hay clic o para reiniciar los gráficos
    empty_pie_especialidades = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)
    empty_pie_sexo = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)
    empty_pie_atendido = px.pie(names=[], values=[], title="Seleccione una barra en el histograma", height=400)

    if clickData is None:
        return empty_pie_especialidades, empty_pie_sexo, empty_pie_atendido

    selected_range = clickData['points'][0]['x']
    filtered_df = df[df['RANGO_DIAS'] == selected_range].copy()

    # --- 1. Gráfico de Pastel de Especialidades (Top 5) ---
    top_especialidades_pie = filtered_df['ESPECIALIDAD'].value_counts().nlargest(5)
    filtered_df['ESPECIALIDAD_AGRUPADA'] = filtered_df['ESPECIALIDAD'].apply(
        lambda x: x if x in top_especialidades_pie.index else 'Otras'
    )
    grouped_especialidades = filtered_df['ESPECIALIDAD_AGRUPADA'].value_counts().reset_index()
    grouped_especialidades.columns = ['ESPECIALIDAD', 'CUENTA']
    fig_especialidades = px.pie(
        grouped_especialidades,
        names='ESPECIALIDAD',
        values='CUENTA',
        title=f"Top 5 Especialidades para el rango '{selected_range}' días",
        height=500
    )
    fig_especialidades.update_traces(textposition='inside', textinfo='percent+label')
    fig_especialidades.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # --- 2. Gráfico de Pastel de Distribución por Sexo ---
    sexo_counts = filtered_df['SEXO'].value_counts().reset_index()
    sexo_counts.columns = ['SEXO', 'CUENTA']
    fig_sexo = px.pie(
        sexo_counts,
        names='SEXO',
        values='CUENTA',
        title=f"Distribución de Sexo para el rango '{selected_range}' días",
        height=500
    )
    fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
    fig_sexo.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # --- 3. Gráfico de Pastel de Distribución Atendido/No Atendido ---
    atendido_counts = filtered_df['ATENDIDO'].value_counts().reset_index()
    atendido_counts.columns = ['ATENDIDO', 'CUENTA']
    fig_atendido = px.pie(
        atendido_counts,
        names='ATENDIDO',
        values='CUENTA',
        title=f"Estado de Atención para el rango '{selected_range}' días",
        height=500
    )
    fig_atendido.update_traces(textposition='inside', textinfo='percent+label')
    fig_atendido.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return fig_especialidades, fig_sexo, fig_atendido


# App 3: Por Modalidad de Cita
app_modalidad = dash.Dash(__name__, server=server, url_base_pathname='/modalidad/')
app_modalidad.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Distribución por Modalidad de Cita", style={'textAlign': 'center'}),
    dcc.Graph(id='pie-modalidad', figure=px.pie(
        df,
        names='PRESENCIAL_REMOTO',
        title='Distribución de Citas: Remotas vs Presenciales',
        template='plotly_white'
    )),
    dcc.Graph(id='bar-especialidad-modalidad', figure=px.bar(
        pd.DataFrame(columns=['ESPECIALIDAD', 'DIFERENCIA_DIAS']),
        x='ESPECIALIDAD',
        y='DIFERENCIA_DIAS',
        title="Seleccione una modalidad en el gráfico de pastel"
    ))
])

@app_modalidad.callback(
    Output('bar-especialidad-modalidad', 'figure'),
    Input('pie-modalidad', 'clickData')
)
def update_bar_modalidad(clickData):
    if clickData is None:
        return px.bar(x=[], y=[], title="Seleccione una modalidad en el gráfico de pastel", height=400)
    
    modalidad = clickData['points'][0]['label']
    filtered_df = df[df['PRESENCIAL_REMOTO'] == modalidad]
    mean_wait = filtered_df.groupby('ESPECIALIDAD')['DIFERENCIA_DIAS'].mean().reset_index()
    mean_wait['DIFERENCIA_DIAS_ROUNDED'] = mean_wait['DIFERENCIA_DIAS'].round().astype(int)
    mean_wait = mean_wait.sort_values(by='DIFERENCIA_DIAS', ascending=False)
    
    # Set bar color based on modality
    bar_color = 'red' if modalidad == 'REMOTO' else '#3498db' # Default blue for 'PRESENCIAL'

    fig = px.bar(
        mean_wait,
        x='ESPECIALIDAD',
        y='DIFERENCIA_DIAS',
        title=f"Media de Días de Espera por Especialidad ({modalidad})",
        labels={'DIFERENCIA_DIAS': 'Días de Espera'},
        template='plotly_white',
        height=500,
        text='DIFERENCIA_DIAS_ROUNDED'
    )
    
    # Update the bar color
    fig.update_traces(marker_color=bar_color, textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig


# App 4: Por Estado de Seguro
app_seguro = dash.Dash(__name__, server=server, url_base_pathname='/asegurados/')
app_seguro.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Distribución por Estado del Seguro", style={'textAlign': 'center'}),
    dcc.Graph(id='pie-seguro', figure=px.pie(
        df.dropna(),
        names='SEGURO',
        title='Distribución de Pacientes: Asegurados vs No Asegurados',
        template='plotly_white'
    )),
    dcc.Graph(id='bar-espera-seguro', figure=px.bar(
        pd.DataFrame(columns=['SEXO', 'DIFERENCIA_DIAS']),
        x='SEXO',
        y='DIFERENCIA_DIAS',
        title="Seleccione una modalidad en el gráfico de pastel"
    ))
])

@app_seguro.callback(
    Output('bar-espera-seguro', 'figure'),
    Input('pie-seguro', 'clickData')
)
def update_bar_seguro(clickData):
    if clickData is None:
        return px.bar(x=[], y=[], title="Seleccione una modalidad en el gráfico de pastel", height=400)
    seguro = clickData['points'][0]['label']
    filtered_df = df[df['SEGURO'] == seguro]
    mean_wait = filtered_df.groupby('SEXO')['DIFERENCIA_DIAS'].mean().reset_index()
    mean_wait['DIFERENCIA_DIAS_ROUNDED'] = mean_wait['DIFERENCIA_DIAS'].round().astype(int)
    mean_wait = mean_wait.sort_values(by='DIFERENCIA_DIAS', ascending=False)
    fig = px.bar(
        mean_wait,
        x='SEXO',
        y='DIFERENCIA_DIAS',
        title=f"Media de Días de Espera por SEXO ({seguro})",
        labels={'DIFERENCIA_DIAS': 'Días de Espera'},
        template='plotly_white',
        height=500,
        text='DIFERENCIA_DIAS_ROUNDED'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_yaxes(range=[18, 21])
    return fig

# App 5: Línea de Tiempo
df['DIA_SOLICITACITA'] = pd.to_datetime(df['DIA_SOLICITACITA'], errors='coerce')
df['MES'] = df['DIA_SOLICITACITA'].dt.to_period('M').astype(str)
citas_por_mes = df.groupby('MES').size().reset_index(name='CANTIDAD_CITAS')


app = dash.Dash(__name__, server=server, url_base_pathname='/tiempo/')
app.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Citas Agendadas por Mes", style={'textAlign': 'center'}),
    dcc.Graph(
        id='grafico-lineal',
        figure=px.line(citas_por_mes, x='MES', y='CANTIDAD_CITAS', markers=True,
                       title='Cantidad de Citas por Mes')
    ),
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-pie-especialidades', style={'height': '400px'})
        ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'}),
        html.Div([
            dcc.Graph(id='grafico-pie-atencion', style={'height': '400px'})
        ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
])

@app.callback(
    [Output('grafico-pie-especialidades', 'figure'),
     Output('grafico-pie-atencion', 'figure')],
    [Input('grafico-lineal', 'clickData')]
)
def actualizar_graficos(clickData):
    if clickData is None:
        return px.pie(names=[], values=[], title="Seleccione un mes"), px.pie(names=[], values=[], title="Seleccione un mes")
    mes_seleccionado = pd.to_datetime(clickData['points'][0]['x']).to_period('M').strftime('%Y-%m')
    df_mes = df[df['MES'] == mes_seleccionado]
    top_especialidades = df_mes['ESPECIALIDAD'].value_counts().nlargest(5)
    df_mes['ESPECIALIDAD_AGRUPADA'] = df_mes['ESPECIALIDAD'].apply(
        lambda x: x if x in top_especialidades.index else 'Otras'
    )
    grouped = df_mes['ESPECIALIDAD_AGRUPADA'].value_counts().reset_index()
    grouped.columns = ['ESPECIALIDAD', 'CUENTA']
    grouped = grouped.sort_values(by='CUENTA', ascending=False)
    
    fig_especialidades = px.pie(grouped, names='ESPECIALIDAD', values="CUENTA", title=f'Distribución de Especialidades en {mes_seleccionado}')
    fig_atencion = px.pie(df_mes, names='ATENDIDO', title=f'Estado de Atención en {mes_seleccionado}')

    return fig_especialidades, fig_atencion

# Ejecutar el servidor
if __name__ == '__main__':
    server.run(debug=True)
