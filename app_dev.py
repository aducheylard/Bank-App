from functools import partial
from tkinter import filedialog
import pandas as pd
import numpy as np
from pandasgui import show
from Class import *
import csv

'''
class Menu:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.value = 10
        self.button = Button(self.master, text='File Search', command='self.getValue')
        self.button.pack()

    def getValue(self):
        print(self.value)
'''


def ask_file_path():
    filename = filedialog.askopenfilename(title="Select file",
                                          filetypes=(("xls files", ['*.xls', '*.xlsx']), ("all files", "*.*")))
    return filename


def excel_to_dataframe():
    global df_ANO_MIXTA
    global df_CMR
    global df_CTA_VISTA
    global df_CTA_CORRIENTE
    filename = ask_file_path()
    #filename = "C:/Users/conej/Desktop/PROYECTOS PYTHON/BANK ACCOUNT/Files/CUENTAS_2020.xlsx"  # todo: eliminar esta linea
    xls = pd.ExcelFile(filename)
    # CARGAMOS CADA PAGINA DEL EXCEL EN UN DF DISTINTO
    df_enero = pd.read_excel(xls, sheet_name='ENERO', skiprows=3)
    df_febrero = pd.read_excel(xls, sheet_name='FEBRERO', skiprows=3)
    df_marzo = pd.read_excel(xls, sheet_name='MARZO', skiprows=3)
    df_abril = pd.read_excel(xls, sheet_name='ABRIL', skiprows=3)
    df_mayo = pd.read_excel(xls, sheet_name='MAYO', skiprows=3)
    df_junio = pd.read_excel(xls, sheet_name='JUNIO', skiprows=3)
    df_julio = pd.read_excel(xls, sheet_name='JULIO', skiprows=3)
    df_agosto = pd.read_excel(xls, sheet_name='AGOSTO', skiprows=3)
    df_septiembre = pd.read_excel(xls, sheet_name='SEPTIEMBRE', skiprows=3)
    df_octubre = pd.read_excel(xls, sheet_name='OCTUBRE', skiprows=3)
    df_noviembre = pd.read_excel(xls, sheet_name='NOVIEMBRE', skiprows=3)
    df_diciembre = pd.read_excel(xls, sheet_name='DICIEMBRE', skiprows=3)

    df_ANO_MIXTA = df_enero.append([df_febrero, df_marzo, df_abril, df_mayo, df_junio, df_julio, df_agosto, df_septiembre, df_octubre, df_noviembre, df_diciembre], sort=False, ignore_index=True)

    # SE BORRAN LOS ESPACIOS ENTRE TABLAS
    df_ANO_MIXTA = df_ANO_MIXTA.drop(df_ANO_MIXTA.columns[[0, 6, 7, 8, 14, 15, 16, 22, 23]], axis=1)
    # SE BORRAN LAS TABLAS 2 Y 3
    df_CTA_VISTA = df_ANO_MIXTA.drop(df_ANO_MIXTA.columns[[5, 6, 7, 8, 9, 10, 11, 12, 13, 14]], axis=1)
    # SE BORRAN LAS TABLAS 1 Y 3
    df_CMR = df_ANO_MIXTA.drop(df_ANO_MIXTA.columns[[0, 1, 2, 3, 4, 10, 11, 12, 13, 14]], axis=1)
    # SE BORRAN LAS TABLAS 1 Y 2
    df_CTA_CORRIENTE = df_ANO_MIXTA.drop(df_ANO_MIXTA.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], axis=1)

    # SE RENOMBRAN LAS COLUMNAS
    df_CTA_VISTA = df_CTA_VISTA.rename(
        columns={'FECHA.1': 'FECHA', 'NOMBRE.1': 'NOMBRE', 'MONTO.1': 'MONTO', 'DESCRIPCION.1': 'DESCRIPCION',
                 'ESTADO.1': 'ESTADO'}, inplace=False)
    df_CMR = df_CMR.rename(
        columns={'FECHA.1': 'FECHA', 'NOMBRE.1': 'NOMBRE', 'MONTO.1': 'MONTO', 'DESCRIPCION.1': 'DESCRIPCION',
                 'ESTADO.1': 'ESTADO'}, inplace=False)
    df_CTA_CORRIENTE = df_CTA_CORRIENTE.rename(
        columns={'FECHA.2': 'FECHA', 'NOMBRE.2': 'NOMBRE', 'MONTO.2': 'MONTO', 'DESCRIPCION.2': 'DESCRIPCION',
                 'ESTADO.2': 'ESTADO'}, inplace=False)

    # SE BORRAN LAS FILAS VACIAS TODO BORRAR LAS FILAS DE FECHAS 'NaT'
    df_CTA_VISTA = df_CTA_VISTA.dropna(subset=['FECHA'])
    df_CMR = df_CMR.dropna(subset=['FECHA'])
    df_CTA_CORRIENTE = df_CTA_CORRIENTE.dropna(subset=['FECHA'])

    # REINICIAMOS LOS INDICES
    df_CTA_VISTA.reset_index(drop=True, inplace=True)
    df_CMR.reset_index(drop=True, inplace=True)
    df_CTA_CORRIENTE.reset_index(drop=True, inplace=True)

    # AGREGA LA COLUMNA 'ABONADO'
    df_CTA_VISTA.insert(2, 'ABONADO', 0)
    df_CMR.insert(2, 'ABONADO', 0)
    df_CTA_CORRIENTE.insert(2, 'ABONADO', 0)

    # RENOMBRAMOS LA COLUMNA 'MONTO' POR 'CARGADO'
    df_CTA_VISTA.rename(columns={"MONTO": "CARGADO"}, inplace=True)
    df_CMR.rename(columns={"MONTO": "CARGADO"}, inplace=True)
    df_CTA_CORRIENTE.rename(columns={"MONTO": "CARGADO"}, inplace=True)

    # ORGANIZAMOS LOS MONTOS DE LAS COMPRAS EN 'ABONADO' Y 'CARGADO'
    df_CTA_VISTA = organiza_valor(df_CTA_VISTA)
    df_CMR = organiza_valor(df_CMR)
    df_CTA_CORRIENTE = organiza_valor(df_CTA_CORRIENTE)

    # GUARDAMOS EL DF A UN CSV
    df_CTA_CORRIENTE.to_csv(path_or_buf='C:/Users/conej/Desktop/PROYECTOS PYTHON/BANK ACCOUNT/Files/csv_final_test',
                            index=False)


def organiza_valor(df):  # SE MUEVEN LOS 'CARGADOS' POSITIVOS HACIA LOS 'ABONADO'
    lista_cargado = df['CARGADO'].to_list()
    lista_abonado = []
    # CONVERTIMOS LOS FLOTANTES A INT TODO CAMBIAR LA COLUMNA 'CARGADO' DEL DF FINAL A INT
    lista_int_cargado = [int(integral) for integral in lista_cargado]

    # SE TRASLADARON LOS DATOS POSITIVOS DE LA COLUMNA 'CARGADO' HACIA LA LISTA 'lista_ABONADO'
    for i in range(lista_int_cargado.__len__()):
        # print(i)
        # print(lista_int_CARGADO[i])
        # SI EL VALOR ES POSITIVO SE INSERTA EN LA LISTA 'lista_int_ABONADO'
        if lista_int_cargado[i] > 0:
            lista_abonado.insert(i, lista_int_cargado[i])
            lista_int_cargado[i] = 0
        else:
            lista_abonado.insert(i, 0)

    # CREAMOS DOS NUEVOS DF TEMPORALES A PARTIR DE LAS LISTAS 'lista_ABONADO' y 'lista_int_CARGADO' PARA ACTUALIZAR EL DF FINAL
    new_df_temp_abonado = pd.DataFrame(lista_abonado, columns=['ABONADO'])
    new_df_temp_cargado = pd.DataFrame(lista_int_cargado, columns=['CARGADO'])

    # ACTUALIZAMOS EL DF FINAL
    df.update(new_df_temp_abonado, overwrite=True)
    df.update(new_df_temp_cargado, overwrite=True)
    return df

'''
def form_crea_account_table():
    root2 = Tk()
    bank_label = Label(root2, text='Banco').grid(row=0, column=0)
    bank = Entry(root2).grid(row=0, column=1)
    tipo_cuenta_label = Label(root2, text='Tipo de Cuenta').grid(row=1, column=0)
    tipo_cuenta = Entry(root2).grid(row=1, column=1)
    numero_cuenta_label = Label(root2, text='Numero de Cuenta').grid(row=2, column=0)
    numero_cuenta = Entry(root2).grid(row=2, column=1)
    nombre_titular_label = Label(root2, text='Nombre').grid(row=3, column=0)
    nombre_titular = Entry(root2).grid(row=3, column=1)
    apellido_titular_label = Label(root2, text='Apellido').grid(row=4, column=0)
    apellido_titular = Entry(root2).grid(row=4, column=1)
    rut_titular_label = Label(root2, text='Rut').grid(row=5, column=0)
    rut_titular = Entry(root2).grid(row=5, column=1)
    submit_button = Button(root2, text='Agregar Cuenta', command=lambda: crea_cuenta(crea_cuenta, bank, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular)).grid(row=6, column=1)



def crea_cuenta(bank, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular):
    print("el banco es: " + str(bank))
    test_cuenta = Cuenta(bank, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular)
    #test_cuenta.showAll()
    print(test_cuenta.banco)


#test = Cuenta('banco', 'tipo_cuenta', 'numero_cuenta', 'nombre_titular', 'apellido_titular', 'rut_titular')
# GUI
root = Tk()
#root.withdraw()
root.geometry('500x500')  # DIMENSIONES DE LA VENTANA
root.title('My Accounts')  # TITULO DE LA VENTANA
search_file_button = Button(root, text='Search File', command=lambda: excel_to_dataframe())  # CREAMOS EL BOTON PARA BUSCAR EL ARCHIVO
search_file_button.pack()

show_df_button = Button(root, text='Show table', command=lambda: show(df_CTA_VISTA, df_CMR, df_CTA_CORRIENTE))  # CREAMOS EL BOTON PARA MOSTRAR LA TABLA
show_df_button.pack()

add_account_table = Button(root, text='Nueva cuenta', command=form_crea_account_table)
add_account_table.pack()

root.mainloop()
'''


# PERMITIMOS MAS INFORMACION EN LA CONSOLA
pd.set_option('display.expand_frame_repr', False)


lista_cuentas = []
menu = Menu()  # INSTANCIAMOS EL MENU
#lista_cuentas.append(menu.cuenta)


tk.mainloop()  # CICLO DE LA GUI TKINTER