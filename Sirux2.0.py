import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox, Tk, PhotoImage, Label
from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt

def seleccionar_archivo():
    global df
    # Abre una ventana para seleccionar el archivo de Excel
    archivo = filedialog.askopenfilename(filetypes=[('Archivos de Excel', '*.xlsx')])
    # Verifica que se haya seleccionado un archivo
    if archivo:
        # Carga el archivo de Excel en un DataFrame
        df = pd.read_excel(archivo)
        # Habilita el menú desplegable para seleccionar la opción de procesamiento
        option_menu.config(state='normal')

def on_option_select(selection):
    global df
    print(f"Opción seleccionada: {selection}")
    if selection == 'OLDELVAL':
        df = generate_oldelval_format(df)
    elif selection == 'YPF':
        df = generate_ypf_format(df)
    elif selection == 'OTASA':
        df = generate_otasa_format(df)
    # Muestra el DataFrame procesado en una tabla
    mostrar_dataframe(df)
    # Habilita el botón de exportación
    export_button.config(state='normal', command=lambda: exportar_archivo(df))

def generate_oldelval_format(df):
    print("Generando formato OLDELVAL")
    #Crear Columnas nuevas
    df['idCaracteristica'] = df["Number"]
    df = df.assign(idEvento="")
    df['nSoldadura'] = df["JointNumber"]
    df["nLongTuboUmt [m]"] = df["LJoint"]
    df["sSubTipo"] = df["FeatureType"]
    df["featureType"] = df["FeatureType"]
    df['featureIdentification'] = df['FeatureIdentification']
    df['AnomalyClass'] = df['AnomalyClass']
    df['nDistanciaRefUmt [m]'] = df["Distance"]
    df['nDSAArUtm [m]'] = df['UpWeld']
    df['nDSAAbUtm [m]'] = df['DownWeld']
    df['nDMAArUtm [m]'] = df['UpMarker']
    df['nDMAAbUtm [m]'] = df['DownMarker']
    df['sPosSolLongUr'] = "" 
    df['nEspParedRefUmm [mm]'] = df['WallThickness']
    df['nProfUmm [mm]'] = ''
    df['nProfUpc [%]'] = df['Depth']
    df['nLongFallaUmm [mm]'] = df['Length']
    df['nAnchoFallaUmm [mm]'] = df['Width']
    df['sCapaFalla'] = df['SurfaceLocation']
    df['sPosicionRelativa'] = df['LocationClass']
    df['sPosFallaUr'] = df['Orientation']
    df['sComentario'] = df['Description']
    df = df.assign(Latitud="")
    df = df.assign(Longitud="")
    df = df.assign(Altura="")
    df['latitud [°]'] = df['Latitud']
    df['longitud [°]'] = df['Longitud']
    df['altura [m]'] = df['Altura']
    df['nProfEfectivaUpc [%]'] = df['EffectiveDepth']
    df['nLongEfectivaUmm [mm]'] = df['EffectiveLength']
    df['nERF AE'] = df['ERFRStreng']
    df['nPF B31G [MPa]'] = df["PBurstB31G"]
    df['nPF 0.85 [MPa]'] = df['PBurstB31GModif']
    df['nPF AE [MPa]'] = df['PBurstRStreng']
    df['nFS B31G'] = df["FSB31G"]
    df['nFS 0.85'] = df['FSB31GModif']
    df['nFS AE'] = df['FSRStreng']
    df['MAPO [MPa]'] = df["MAOP"]

    #Elimina los datos nulos
    df['AnomalyClass'] = df['AnomalyClass'].replace('Unknown', '')
    df['AnomalyClass'] = df['AnomalyClass'].replace('Pitting', 'PITT')
    df['AnomalyClass'] = df['AnomalyClass'].replace('General', 'GENE')
    df['AnomalyClass'] = df['AnomalyClass'].replace('Pinhole', 'PINH')
    df['AnomalyClass'] = df['AnomalyClass'].replace('AxialGrooving', 'AXGR')
    df['AnomalyClass'] = df['AnomalyClass'].replace('AxialSlotting', 'AXSL')
    df['AnomalyClass'] = df['AnomalyClass'].replace('CircumferentialGrooving', 'CIGR')
    df['AnomalyClass'] = df['AnomalyClass'].replace('CircumferentialSlotting', 'CISL')
    df['nEspParedRefUmm [mm]'] = df['nEspParedRefUmm [mm]'].replace('0,00', '')
    df['nProfUpc [%]'] = df['nProfUpc [%]'].replace('0,00', '')
    df['nLongEfectivaUmm [mm]'] = df['nLongEfectivaUmm [mm]'].replace(0, '')
    df["nProfEfectivaUpc [%]"] = df["nProfEfectivaUpc [%]"].replace('0,00', '')
    df["nERF AE"] = df["nERF AE"].replace('0,00', '')
    df["nPF B31G [MPa]"] = df["nPF B31G [MPa]"].replace('0,00', '')
    df["nPF 0.85 [MPa]"] = df["nPF 0.85 [MPa]"].replace('0,00', '')
    df["nPF AE [MPa]"] = df["nPF AE [MPa]"].replace('0,00', '')
    df["nFS B31G"] = df["nFS B31G"].replace('0,00', '')
    df["nFS 0.85"] = df["nFS 0.85"].replace('0,00', '')
    df["nFS AE"] = df["nFS AE"].replace('0,00', '')
    df["MAPO [MPa]"] = df["MAPO [MPa]"].replace('0,00', '')

    def reemplazar_valor(row):
        if row['nLongFallaUmm [mm]'] == 5 and row['nAnchoFallaUmm [mm]'] == 5:
            return ''
        else:
            return row['nLongFallaUmm [mm]']

# Aplica la función a cada fila y guarda el resultado en las columnas 'A' y 'B'
    df['nLongFallaUmm [mm]'] = df.apply(reemplazar_valor, axis=1)
    df['nAnchoFallaUmm [mm]'] = df.apply(reemplazar_valor, axis=1)
        

    #Pasar Cluster con definicion metalloss/millfault
    def completar_sSubTipo(row):
        if row['featureType'] == 'Cluster' and row['featureIdentification'] == 'Metalloss':
            return 'ClusterMetalloss'
        elif row['featureType'] == 'Cluster' and row['featureIdentification'] == 'MillFault':
            return 'ClusterMillFault'
        else:
            return row['sSubTipo']

    # Aplica la función a cada fila y guarda el resultado en la columna 'sSubTipo'
    df['sSubTipo'] = df.apply(completar_sSubTipo, axis=1)

    # Crea un diccionario con las palabras y sus traducciones
    traducciones = {
            'Weld': 'SOLDADURA',
            'Metalloss': 'PERDIDA DE METAL',
            'MillFault': 'ANOMALIA DE MANUFACTURA',
            'Tee': 'DERIVACION',
            'Tap': 'TOMA',
            'OffTake': 'TOMA FORJADA',
            'BendRight': 'CURVA',
            'ClusterMetalloss': 'PERDIDA DE METAL-CLUSTER',
            'ClusterMillFault': 'ANOMALIA DE MANUFACTURA-CLUSTER',
            'Flange': 'BRIDA',
            'Dent': 'ABOLLADURA',
            'Support': 'SOPORTE',
            'SupportFullCircular': 'SOPORTE CIRCUNFERENCIAL',
            'SupportGroundAnchor': 'SOPORTE SEMI-CIRCUNFERENCIAL',
            'Valve': 'VALVULA',
            'UnknownFeature': 'OBJETO DESCONOCIDO',
            'MetalObject': 'OBJETO METALICO',
            'RepairPatch': 'REPARACION PARCHE',
            'RepairPatchBegin': 'REPARACION MEDIA CAÑA-INICIO',
            'RepairPatchEnd': 'REPARACION MEDIA CAÑA-FIN',
            'BendLeft': 'CURVA',
            'BendDown': 'CURVA',
            'BendUp': 'CURVA',
            "CasingBegin" : "CAÑO CAMISA-INICIO" ,
            "CasingEnd" : "CAÑO CAMISA-FIN"
        }

    # Reemplaza las palabras en la columna deseada
    df['sSubTipo'] = df['sSubTipo'].replace(traducciones)

    # Completa las celdas vacias (COMPLETAR CON LOS VALORES PARA ORDENAR EL EXCEL CON LOS DATOS REQUERIDOS)
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'featureType'] = 'WELD'
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'featureIdentification'] = 'ERW Pipe'
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'idEvento'] = '401'
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'nDSAArUtm [m]'] = '0,00'
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'nDSAAbUtm [m]'] = '0,00'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL', 'featureType'] = 'ANOM'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL', 'featureIdentification'] = 'CORR'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL', 'idEvento'] = '102'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA', 'featureType'] = 'ANOM'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA', 'featureIdentification'] = 'MIAN'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA', 'idEvento'] = '101'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'featureType'] = 'ANOM'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'featureIdentification'] = 'COCL'
    df.loc[df['sSubTipo'] == 'PERDIDA DE METAL-CLUSTER', 'idEvento'] = '102'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'featureType'] = 'ANOM'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'featureIdentification'] = 'MACL'
    df.loc[df['sSubTipo'] == 'ANOMALIA DE MANUFACTURA-CLUSTER', 'idEvento'] = '101'
    df.loc[df['sSubTipo'] == 'ABOLLADURA', 'featureType'] = 'ANOM'
    df.loc[df['sSubTipo'] == 'ABOLLADURA', 'featureIdentification'] = 'DENP'
    df.loc[df['sSubTipo'] == 'ABOLLADURA', 'idEvento'] = '103'
    df.loc[df['sSubTipo'] == 'ABOLLADURA', 'AnomalyClass'] = ''
    df.loc[df['sSubTipo'] == 'VALVULA', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'VALVULA', 'featureIdentification'] = 'VALV'
    df.loc[df['sSubTipo'] == 'VALVULA', 'idEvento'] = '302'
    df.loc[df['sSubTipo'] == 'DERIVACION', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'DERIVACION', 'featureIdentification'] = 'TEE'
    df.loc[df['sSubTipo'] == 'DERIVACION', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'TOMA', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'TOMA', 'featureIdentification'] = 'OFFT'
    df.loc[df['sSubTipo'] == 'TOMA', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'TOMA FORJADA', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'TOMA FORJADA', 'featureIdentification'] = 'HTAP'
    df.loc[df['sSubTipo'] == 'TOMA FORJADA', 'idEvento'] = '304'
    df.loc[df['sSubTipo'] == 'BRIDA', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'BRIDA', 'featureIdentification'] = 'FLG'
    df.loc[df['sSubTipo'] == 'BRIDA', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'AGM', 'featureType'] = 'MARK'
    df.loc[df['sSubTipo'] == 'AGM', 'featureIdentification'] = "AGM"
    df.loc[df['sSubTipo'] == 'AGM', 'idEvento'] = '502'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'featureType'] = 'REPA'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'featureIdentification'] = 'WSLB'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-INICIO', 'idEvento'] = '201'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'featureType'] = 'REPA'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'featureIdentification'] = 'WSLE'
    df.loc[df['sSubTipo'] == 'REPARACION MEDIA CAÑA-FIN', 'idEvento'] = '201'
    df.loc[df['sSubTipo'] == 'REPARACION PARCHE', 'featureType'] = 'REPA'
    df.loc[df['sSubTipo'] == 'REPARACION PARCHE', 'featureIdentification'] = 'PATC'
    df.loc[df['sSubTipo'] == 'REPARACION PARCHE', 'idEvento'] = '303'
    df.loc[df['sSubTipo'] == 'CURVA', 'featureType'] = 'OTHE'
    df.loc[df['sSubTipo'] == 'CURVA', 'featureIdentification'] = 'BEND'
    df.loc[df['sSubTipo'] == 'CURVA', 'idEvento'] = '601'
    df.loc[df['sSubTipo'] == 'OBJETO METALICO', 'featureType'] = 'ADME'
    df.loc[df['sSubTipo'] == 'OBJETO METALICO', 'featureIdentification'] = 'CLMO'
    df.loc[df['sSubTipo'] == 'OBJETO METALICO', 'idEvento'] = '105'
    df.loc[df['sSubTipo'] == 'OBJETO DESCONOCIDO', 'featureType'] = 'OTHE'
    df.loc[df['sSubTipo'] == 'OBJETO DESCONOCIDO', 'featureIdentification'] = 'OTHE'
    df.loc[df['sSubTipo'] == 'OBJETO DESCONOCIDO', 'idEvento'] = '305'
    df.loc[df['sSubTipo'] == 'SOPORTE', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'SOPORTE', 'featureIdentification'] = 'ESUP'
    df.loc[df['sSubTipo'] == 'SOPORTE', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'featureIdentification'] = 'ANCH'
    df.loc[df['sSubTipo'] == 'SOPORTE SEMI-CIRCUNFERENCIAL', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'featureIdentification'] = ''
    df.loc[df['sSubTipo'] == 'SOPORTE CIRCUNFERENCIAL', 'idEvento'] = '301'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-INICIO', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-INICIO', 'featureIdentification'] = 'CASB'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-INICIO', 'idEvento'] = '305'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-FIN', 'featureType'] = 'COMP'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-FIN', 'featureIdentification'] = 'CASE'
    df.loc[df['sSubTipo'] == 'CAÑO CAMISA-FIN', 'idEvento'] = '305'

    columnas = ["nProfEfectivaUpc [%]", "nLongEfectivaUmm [mm]","nERF AE", "nPF B31G [MPa]", "nPF 0.85 [MPa]", "nPF AE [MPa]", "nFS B31G", "nFS 0.85", "nFS AE", "MAPO [MPa]"]
    df.loc[df['sSubTipo'] == 'ABOLLADURA', columnas] = ""

    #Traer la orientacion de la soldadura
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'sPosSolLongUr'] = df['sPosFallaUr']
    df.loc[df['sSubTipo'] == 'SOLDADURA', 'sPosFallaUr'] = ''

#Pega el valor de orientacion de las soldaduras en las anomalias
    ultimo_valor = ''
    for index, row in df.iterrows():
        if row['sSubTipo'] == 'SOLDADURA':
            ultimo_valor = row['sPosSolLongUr']
        elif row['sSubTipo'] in ['PERDIDA DE METAL', 'PERDIDA DE METAL-CLUSTER', 'ANOMALIA DE MANUFACTURA', 'ANOMALIA DE MANUFACTURA-CLUSTER']:
            df.loc[index, 'sPosSolLongUr'] = ultimo_valor   

    #Seleccionar solo las columnas que quiero
    df = df[["idCaracteristica", "idEvento", "nSoldadura", "nLongTuboUmt [m]", "sSubTipo", "featureType",  "featureIdentification", "AnomalyClass", "nDistanciaRefUmt [m]" ,
                 "nDSAArUtm [m]", "nDSAAbUtm [m]", "nDMAArUtm [m]", "nDMAAbUtm [m]", "sPosSolLongUr", "nEspParedRefUmm [mm]", "nProfUmm [mm]", "nProfUpc [%]", "nLongFallaUmm [mm]", "nAnchoFallaUmm [mm]", 
                 "sCapaFalla", "sPosicionRelativa", "sPosFallaUr", "sComentario", "latitud [°]", "longitud [°]", "altura [m]", "nProfEfectivaUpc [%]", "nLongEfectivaUmm [mm]",
                   "nERF AE", "nPF B31G [MPa]", "nPF 0.85 [MPa]", "nPF AE [MPa]", "nFS B31G", "nFS 0.85", "nFS AE", "MAPO [MPa]"]]
    
    graph_button.config(state='normal')

    return df

def generate_ypf_format(df):
    # Procesa el DataFrame para la opción YPF aquí
    # ...
    return df

def generate_otasa_format(df):
    # Procesa el DataFrame para la opción OTASA aquí
    # ...
    return df

def mostrar_dataframe(df):
    # Muestra el DataFrame en una tabla aquí
    # Crea un widget de tabla para mostrar el archivo traducido
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    table = Table(frame)
    table.show()

    # Muestra el archivo traducido en el widget de tabla
    table.model.df = df
    table.redraw()

def exportar_archivo(df):
    # Abre una ventana de diálogo para guardar el archivo
    ruta = filedialog.asksaveasfilename(filetypes=[('Archivos de Excel', '*.xlsx')], defaultextension='.xlsx')
    # Verifica que se haya seleccionado una ruta
    if ruta:
        # Guarda el archivo en la ruta seleccionada
        df.to_excel(ruta, index=False)
        messagebox.showinfo('Exportación exitosa', 'Listo')

def mostrar_grafico():    
    global df
    eg=df[["sSubTipo", "nDistanciaRefUmt [m]", "nFS AE", "nEspParedRefUmm [mm]", "nProfUpc [%]"]]
    eg.loc[:, 'unos'] = 1
        # Crea una lista con los valores que deseas mantener
    valores = ["PERDIDA DE METAL", "ANOMALIA DE MANUFACTURA", "VALVULA", "AGM"]

        # Filtra el DataFrame para mantener solo las filas con los valores deseados en la columna 'sSubTipo'
    eg = eg[eg['sSubTipo'].isin(valores)]
    eg["nProfUpc [%]"] = eg["nProfUpc [%]"].str.replace(',', '.')
    eg["nProfUpc [%]"] = pd.to_numeric(eg["nProfUpc [%]"], errors='coerce') / 100
    eg["nDistanciaRefUmt [m]"] = eg["nDistanciaRefUmt [m]"].str.replace(',', '.')
    eg["nDistanciaRefUmt [m]"] = pd.to_numeric(eg["nDistanciaRefUmt [m]"], errors='coerce')
    eg["nFS AE"] = eg["nFS AE"].str.replace(',', '.')
    eg["nFS AE"] = pd.to_numeric(eg["nFS AE"], errors='coerce')
    eg["nEspParedRefUmm [mm]"] = eg["nEspParedRefUmm [mm]"].str.replace(',', '.')
    eg["nEspParedRefUmm [mm]"] = pd.to_numeric(eg["nEspParedRefUmm [mm]"], errors='coerce')

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

# Crea el primer gráfico utilizando el objeto 'ax1'
    ultimo_valor = eg["nDistanciaRefUmt [m]"].iloc[-1]
    ax1.grid(True, linestyle='--', color='lightgrey')
    ax1.plot([0, ultimo_valor], [1, 1], color='k', linestyle='-', label="Tuberia", linewidth=0.8)
    ax1.plot([0, 0], [0.95, 1.05], color='k')
    ax1.plot([ultimo_valor, ultimo_valor], [0.95, 1.05], color='k')
    ax1.scatter(eg["nDistanciaRefUmt [m]"], eg["nProfUpc [%]"], color='#9F3C3C', label="Profundidad", marker="x")
    ax1.scatter(eg["nDistanciaRefUmt [m]"], eg["nFS AE"], color='#7FC8EA', label="FS", marker="x")
    mask_valvula = eg["sSubTipo"] == "VALVULA"
    ax1.scatter(eg.loc[mask_valvula, "nDistanciaRefUmt [m]"], eg.loc[mask_valvula, 'unos'], color='#2AD24B', label="Valvula", marker="^", s=100)
    mask_agm = eg["sSubTipo"] == "AGM"
    ax1.scatter(eg.loc[mask_agm, "nDistanciaRefUmt [m]"], eg.loc[mask_agm, 'unos'], color='#C8C948', label="AGM", marker="p", s=70)
    ax1.set_yticks(list(np.arange(0, 1 + 0.2, 0.2)) + list(np.arange(0, 3.6 + 0.2, 0.2)))
    ax1.set_yticklabels(['{:,.0%}'.format(tick) if tick < 1 else round(tick, 2) for tick in ax1.get_yticks()])
    ax1.set_title("Distribucion de Anomalias por Profundidad y  FS")

    # Agrega las etiquetas a los ejes x e y
    ax1.set_ylabel("Prof.[%]        <|>            Factor de Seguridad                     ")
    ax1.tick_params(axis='x', which='major', pad=20)

# Crea el segundo gráfico utilizando el objeto 'ax2'
    ax2.plot(eg["nDistanciaRefUmt [m]"], eg["nEspParedRefUmm [mm]"], color= "#F1864C", label="Espesor")
    ax2.grid(True, linestyle='--', color='lightgrey')
    ax2.set_yticks([5.56, 6.35, 7.92, 9.52,11.11])
    ax2.xaxis.set_ticks_position('top')

    # Agrega las etiquetas a los ejes x e y
    ax2.set_xticklabels([])
    ax2.set_xlabel("Distancia [m]")
    ax2.set_ylabel("Espesor [mm]")

# Muestra la leyenda
    ax1.legend()
    ax2.legend()

    # Muestra la leyenda
    plt.legend()
    # Muestra el gráfico
    plt.show()


    
# Crea la ventana principal
root = Tk()
root.title('Sirux')
root.iconbitmap('Miproyecto.ico')
root.geometry("800x600")
imagen = PhotoImage(file="Sirux.png")
background = Label(image=imagen)
background.place(x=0, y=0, relwidth=1, relheight=1)
background.config(bg="#0E2F54")

# Maximiza la ventana para adaptarse a la resolución del monitor
root.state('zoomed')

# Crea un marco para contener los botones
button_frame = tk.Frame(root)
button_frame.pack(side='top', fill='x', anchor='center') # Centra el marco en la parte superior de la ventana
button_frame.config(bg="#0E2F54")

# Crea un marco adicional para contener los botones
inner_frame = tk.Frame(button_frame)
inner_frame.pack(side='top', anchor='center') # Centra el marco adicional en el marco button_frame

# Crea un botón para seleccionar el archivo
boton = tk.Button(inner_frame, text='Seleccionar Archivo Excel', command=seleccionar_archivo, bg="#0E2F54", fg="white")
boton.pack(side='left')

# Crea un menú desplegable para seleccionar la opción de procesamiento
options = ['OLDELVAL', 'YPF', 'OTASA']
option_var = tk.StringVar(root)
option_var.set(options[0])
option_menu = tk.OptionMenu(inner_frame, option_var, *options)
option_menu.config(bg="#0E2F54", fg="white")
option_menu.pack(side='left')
option_var.trace('w', lambda *args: on_option_select(option_var.get()))

#Boton de Exportacion
export_button = tk.Button(inner_frame, text="Exportar", state='disabled', bg="#0E2F54", fg="white")
export_button.pack(side='left')

# Crea un botón para mostrar el gráfico
graph_button = tk.Button(inner_frame, text='Grafico', command=mostrar_grafico, state="disabled" )
graph_button.pack(side='left')

#Boton de salir
exit_button = tk.Button(inner_frame, text="Salir", command=root.quit, bg="#0E2F54", fg="white")
exit_button.pack(side='left')

# Inicia el bucle principal
root.mainloop()