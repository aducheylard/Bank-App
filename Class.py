import csv
import os
import tkinter as tk
import sys
import pandas as pd
from tkintertable.Tables import TableCanvas  # http://dmnfarrell.github.io/tkintertable/index.html
from tkintertable.TableModels import TableModel
from functools import partial


class App(tk.Tk):
    def __init__(self):
        #menu = Menu()
        pass


class Menu:
    #lista_cuentas = []  # LISTA DE CUENTAS AGREGADAS

    def __init__(self):
        self.menu_window = tk.Tk()
        #self.cuenta = None
        self.menu_gui()
        self.nombre_archivo_cuentas = 'Datos_Cuenta.csv'
        self.nombre_archivo_transacciones = 'Historial_transacciones.csv'
        self.lista_tipo_cuenta = ['Cta. Corriente', 'Cta. Vista', 'Cta. Ahorro', 'Chequera Electronica']  # TIPOS DE CUENTAS

    def menu_gui(self):
        self.menu_window.title('Cuentas')
        self.menu_window.geometry('500x500')
        self.menu_window.focus_force()
        self.menu_window.nueva_cuenta_button = tk.Button(self.menu_window, text='Nueva cuenta', command=self.crear_cuenta_form)
        self.menu_window.nueva_cuenta_button.pack()
        self.menu_window.abrir_cuenta_button = tk.Button(self.menu_window, text='Abrir Cuenta', command=lambda: self.abrir_cuenta(self.menu_window))
        self.menu_window.abrir_cuenta_button.pack()
        self.menu_window.borrar_todo_button = tk.Button(self.menu_window, text='Borrar todas las cuentas', command=self.borrar_todo_popup)
        self.menu_window.borrar_todo_button.pack()
        self.menu_window.cerrar = tk.Button(text='Cerrar', command=self.menu_window.destroy)
        self.menu_window.cerrar.pack()

    def borrar_todo_popup(self):
        borrar_todo_confirmation_win = tk.Toplevel(self.menu_window)
        borrar_todo_confirmation_win.geometry('500x500')
        borrar_todo_confirmation_win.focus_force()
        text_label = tk.Label(borrar_todo_confirmation_win, text='Seguro que desea borrar todas sus cuentas y transacciones?')
        text_label.grid(row=0, column=0)
        confirmation_button = tk.Button(borrar_todo_confirmation_win, text='SI', command=lambda: self.borrar_archivo(borrar_todo_confirmation_win, self.nombre_archivo_cuentas))
        confirmation_button.grid(row=1, column=0)
        negation_button = tk.Button(borrar_todo_confirmation_win, text='NO', command=borrar_todo_confirmation_win.destroy)
        negation_button.grid(row=2, column=0)

    def borrar_archivo(self, popup, archivo):
        if self.existe_archivopip in(archivo):
            os.remove(archivo)
        else:
            print("El archivo no se puede borrar porque no existe")
        popup.destroy()

    def crear_cuenta_form(self):
        nueva_cuenta_win = tk.Toplevel(self.menu_window)
        nueva_cuenta_win.title('Nueva Cuenta')
        nueva_cuenta_win.geometry('500x500')
        nueva_cuenta_win.focus_force()
        banco_label = tk.Label(nueva_cuenta_win, text='Banco')
        banco_label.grid(row=0, column=0)
        banco = tk.Entry(nueva_cuenta_win)
        banco.grid(row=0, column=1)
        tipo_cuenta_label = tk.Label(nueva_cuenta_win, text='Tipo de Cuenta')
        tipo_cuenta_label.grid(row=1, column=0)
        tipo_cuenta_default = tk.StringVar(nueva_cuenta_win)  # AQUI SE GUARDA EL VALOR DEL MENU
        tipo_cuenta_default.set(self.lista_tipo_cuenta[0])  # POR DEFECTO EL TIPO DE CUENTA ES EL PRIMERO DE LA LISTA
        tipo_cuenta_opt = tk.OptionMenu(nueva_cuenta_win, tipo_cuenta_default, *self.lista_tipo_cuenta)
        tipo_cuenta_opt.grid(row=1, column=1)
        #tipo_cuenta = tk.Entry(nueva_cuenta_win)
        #tipo_cuenta.grid(row=1, column=1)
        numero_cuenta_label = tk.Label(nueva_cuenta_win, text='Numero de Cuenta')
        numero_cuenta_label.grid(row=2, column=0)
        numero_cuenta = tk.Entry(nueva_cuenta_win)
        numero_cuenta.grid(row=2, column=1)
        nombre_titular_label = tk.Label(nueva_cuenta_win, text='Nombre')
        nombre_titular_label.grid(row=3, column=0)
        nombre_titular = tk.Entry(nueva_cuenta_win)
        nombre_titular.grid(row=3, column=1)
        apellido_titular_label = tk.Label(nueva_cuenta_win, text='Apellido')
        apellido_titular_label.grid(row=4, column=0)
        apellido_titular = tk.Entry(nueva_cuenta_win)
        apellido_titular.grid(row=4, column=1)
        rut_titular_label = tk.Label(nueva_cuenta_win, text='Rut')
        rut_titular_label.grid(row=5, column=0)
        rut_titular = tk.Entry(nueva_cuenta_win)
        rut_titular.grid(row=5, column=1)
        submit_button = tk.Button(nueva_cuenta_win, text='Agregar Cuenta', command=lambda: self.guarda_cuenta_csv(banco.get(), tipo_cuenta_default.get(), numero_cuenta.get(), nombre_titular.get(), apellido_titular.get(), rut_titular.get()))
        submit_button.grid(row=6, column=1)
        exit_button = tk.Button(nueva_cuenta_win, text='Cerrar', command=nueva_cuenta_win.destroy)
        exit_button.grid(row=6, column=2)

    def abrir_cuenta(self, menu_window):
        df_datos_cuenta = self.archivo_to_df(self.nombre_archivo_cuentas)
        print(df_datos_cuenta)
        abrir_cuenta_win = tk.Toplevel(menu_window)
        abrir_cuenta_win.title('Abrir Cuenta')
        abrir_cuenta_win.geometry('500x500')
        abrir_cuenta_win.focus_force()
        # TODO: ARREGLAR EL PASO DEL ARGUMENTO DEL INDEX AL HISTORIAL_TRANSACCIONES
        # TODO: CADA VEZ QUE CREO UN BOTON NO TENGO FORMA DE PASARLE EL IDENTIFICADOR DE LA CUENTA Q QUIERO ABRIR A LA FUNCION HISTORIAL TRANSACCIONES
        indice_boton = []  # CREAMOS UNA LISTA PARA ALMACENAR LAS DIRECCINES DE LOS BOTONES
        for row in df_datos_cuenta.itertuples():
            index, id, banco, cta, la, lala, lalala, lalalala = row
            # print(row)
            #lista_cuentas.append(row)
            cuenta_numero_i_button = tk.Button(abrir_cuenta_win, text=row.BANCO + '\n' + row.TIPO_CUENTA, width=20, command=partial(self.historial_transacciones, abrir_cuenta_win, row.ID))
            cuenta_numero_i_button.pack()
            indice_boton.append(cuenta_numero_i_button)  # AGREGAMOS A LA LISTA DE DIRECCIONES DE LOS BOTONES LOS BOTONES
            # AQUI COMO EJEMPLO PODEMOS MODIFICAR EL TEXTO DE UN BOTON EN FUNCION DE SU DIRECCION
            # nombre_boton = (indice_boton[n])
            # nombre_boton.configure(text = "clicked")
        atras_button = tk.Button(abrir_cuenta_win, text='Atras', command=abrir_cuenta_win.destroy)
        atras_button.pack()

    def historial_transacciones(self, abrir_cuenta_win, id_cuenta):
        # TODO: ABRIR EL CSV DE TRANSACCIONES Y GUARDARLO EN UN DF
        print("RECIBI EL ID DE LA CUENTA", id_cuenta)
        indice_cuenta = id_cuenta - 1  # COMO LA FUNCION RECIBE EL ID Y NO EL INDICE DEL DF DE LAS CUENTAS TENEMOS QUE RESTARLE 1
        df_datos_cuenta = self.archivo_to_df(self.nombre_archivo_cuentas)
        # VENTANA PRINCIPAL DEL HISTORIAL DE TRANSACCIONES
        transacciones_win = tk.Toplevel(abrir_cuenta_win)
        transacciones_win.geometry('700x500')
        transacciones_win.title('Transacciones ' + df_datos_cuenta.iloc[indice_cuenta, 2] + ', ' + df_datos_cuenta.iloc[indice_cuenta, 1])
        # LABEL VENTANA
        nombre_win = tk.Label(transacciones_win, text='Transacciones ' + df_datos_cuenta.iloc[indice_cuenta, 2] + ', ' + df_datos_cuenta.iloc[indice_cuenta, 1])
        nombre_win.grid(row=0, column=1)
        # MOSTRAMOS LA TABLA DE LAS TRANSACCIONES
        self.mostrar_tabla(transacciones_win, id_cuenta)
        # BOTON PARA CREAR UNA NUEVA TRANSACCION
        nueva_transaccion_button = tk.Button(transacciones_win, text='Nueva Transaccion', command=lambda: self.nueva_transaccion(transacciones_win, df_datos_cuenta, indice_cuenta))
        nueva_transaccion_button.grid(row=1, column=1)
        # BOTON PARA ACTUALIZAR LA TABLA DE TRANSACCIONES
        # TODO: EL ACUTALIZAR LA TABLA NO FUNCIONA, HAY QUE VOLVER A IMPORTAR DEL CSV
        nueva_transaccion_button = tk.Button(transacciones_win, text='Actualizar Transferencias', command=lambda: self.mostrar_tabla(transacciones_win, id_cuenta))
        nueva_transaccion_button.grid(row=1, column=2)
        # BOTON PARA REGRESAR A LA VENTANA ANTERIOR
        atras_button = tk.Button(transacciones_win, text='Atras', command=transacciones_win.destroy)
        atras_button.grid(row=3, column=2)

    def mostrar_tabla(self, transacciones_win, id_cuenta):
        print("El id_cuenta es ", id_cuenta)
        # SETEAMOS LA TABLA Y SUS PROPIEDADES
        # GUI TABLA
        # TODO: HACER LA TABLA MAS BONITA
        frame = tk.Frame(transacciones_win)
        frame.grid(row=2, column=1)
        # PASAMOS LAS TRANSACCIONES A UN DF
        df_transacciones = self.archivo_to_df(self.nombre_archivo_transacciones)
        # GUARDAMOS EL FILTRO DEL DF A PARTIR DEL 'id_cuenta' QUE BUSCAMOS.
        filtro = df_transacciones['ID_CUENTA'] == id_cuenta
        # print(df_transacciones[filtro])
        # PASAMOS EL DF A UN DICTIONARY
        dic = df_transacciones[filtro].to_dict('index')
        # FORMATO TIPO DEL DICCIONARIO QUE RECIBE LA TABLA
        # dic_example = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}}
        # DEFINIMOS LA TABLA
        table = TableCanvas(frame, data=dic)
        table.show()

    # TODO: LEER TRANSACCIONES DEL CSV
    def abrir_transacciones(self):
        pass

    def nueva_transaccion(self, transacciones_o_menu_win, df_datos_cuenta, indice_cuenta):  # SI CREO LA TRANSACCION DESDE EL MENU PRINCIPAL EL 'df_datos_cuenta' Y 'fila_df' DEBEN SER NONE
        nueva_transaccion_win = tk.Toplevel(transacciones_o_menu_win)
        nueva_transaccion_win.title('Nueva Transaccion')
        nueva_transaccion_win.geometry('500x500')
        nueva_transaccion_label = tk.Label(nueva_transaccion_win, text='Nueva Transaccion')
        nueva_transaccion_label.grid(row=0, column=1)
        #else:  # SI CREO LA TRANSACCION DESDE EL HISTORIAL DE LAS TRANSACCIONES
        # TIPO DE CUENTA
        tipo_cuenta_label = tk.Label(nueva_transaccion_win, text='Tipo de Cuenta')
        tipo_cuenta_label.grid(row=2, column=0)
        tipo_cuenta_entry_default = tk.StringVar(nueva_transaccion_win)  # AQUI SE GUARDA EL VALOR DEL MENU
        tipo_cuenta_entry_default.set(df_datos_cuenta.iloc[indice_cuenta, 2])  # POR DEFECTO EL TIPO DE CUENTA ES EL PRIMERO DE LA LISTA
        tipo_cuenta_opt = tk.OptionMenu(nueva_transaccion_win, tipo_cuenta_entry_default, *self.lista_tipo_cuenta)
        tipo_cuenta_opt.config(state='disabled')
        tipo_cuenta_opt.grid(row=2, column=1)
        # BANCO
        banco_entry = tk.Entry(nueva_transaccion_win)
        banco_label = tk.Label(nueva_transaccion_win, text='Banco')
        banco_label.grid(row=1, column=0)
        banco_entry_default = tk.StringVar(nueva_transaccion_win)
        banco_entry_default.set(df_datos_cuenta.iloc[indice_cuenta, 1])
        banco_entry.config(textvariable=banco_entry_default, state='disabled')
        banco_entry.grid(row=1, column=1)
        # NUMERO DE CUENTA
        numero_cuenta_label = tk.Label(nueva_transaccion_win, text='Numero cuenta')
        numero_cuenta_label.grid(row=3, column=0)
        numero_cuenta_entry = tk.Entry(nueva_transaccion_win)
        numero_cuenta_default = tk.StringVar(nueva_transaccion_win)
        numero_cuenta_default.set(df_datos_cuenta.iloc[indice_cuenta, 3])
        numero_cuenta_entry.config(textvariable=numero_cuenta_default, state='disabled')
        numero_cuenta_entry.grid(row=3, column=1)
        # FECHA
        fecha_label = tk.Label(nueva_transaccion_win, text='FECHA')
        fecha_label.grid(row=4, column=0)
        fecha_entry = tk.Entry(nueva_transaccion_win)
        fecha_entry.grid(row=4, column=1)
        # NOMBRE DE LA COMPRA
        nombre_compra_label = tk.Label(nueva_transaccion_win, text='NOMBRE COMPRA')
        nombre_compra_label.grid(row=5, column=0)
        nombre_compra_entry = tk.Entry(nueva_transaccion_win)
        nombre_compra_entry.grid(row=5, column=1)
        # MONTO
        monto_label = tk.Label(nueva_transaccion_win, text='MONTO')
        monto_label.grid(row=6, column=0)
        monto_entry = tk.Entry(nueva_transaccion_win)
        monto_entry.grid(row=6, column=1)
        # DESCRIPCION
        descripcion_label = tk.Label(nueva_transaccion_win, text='DESCRIPCION')
        descripcion_label.grid(row=7, column=0)
        descripcion_entry = tk.Entry(nueva_transaccion_win)
        descripcion_entry.grid(row=7, column=1)
        # NOMBRE COMPRADOR
        nombre_comprador_label = tk.Label(nueva_transaccion_win, text='NOMBRE COMPRADOR')
        nombre_comprador_label.grid(row=8, column=0)
        nombre_comprador_entry = tk.Entry(nueva_transaccion_win)
        nombre_comprador_entry.grid(row=8, column=1)
        # ESTADO DE LA TRANSACCION (NO PAGADO/PAGADO)
        estado_label = tk.Label(nueva_transaccion_win, text='ESTADO')
        estado_label.grid(row=9, column=0)
        estado_entry = tk.Entry(nueva_transaccion_win)
        estado_entry.grid(row=9, column=1)
        # BOTON AGREGAR LA TRANSACCION
        agregar_transaccion_button = tk.Button(nueva_transaccion_win, text='Agregar Transaccion', command=lambda: self.guarda_transaccion_csv(indice_cuenta + 1, fecha_entry.get(), nombre_compra_entry.get(), monto_entry.get(), descripcion_entry.get(), nombre_comprador_entry.get(), estado_entry.get()))
        agregar_transaccion_button.grid(row=10, column=1)
        # BOTON PARA CERRAR LA VENTANA Y VOLVER ATRAS
        atras_button = tk.Button(nueva_transaccion_win, text='Atras', command=nueva_transaccion_win.destroy)
        atras_button.grid(row=10, column=2)

    def guarda_transaccion_csv(self, id_cuenta, fecha, nombre_compra, monto, descripcion, nombre_comprador, estado):
        with open(self.nombre_archivo_transacciones, mode='a', newline='') as archivo:  # mode='a|w' 'a' PARA NO TRUNCAR EL ARCHIVO Y 'w' PARA TRUNCAR
            writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            if self.existe_archivo(self.nombre_archivo_transacciones):  # SI EXISTE EL ARCHIVO
                if self.file_empty(self.nombre_archivo_transacciones):  # SI EXISTE EL ARCHIVO PERO ESTA VACIO
                    writer.writerow(['ID', 'ID_CUENTA', 'FECHA', 'NOMBRE_COMPRA', 'MONTO', 'DESCRIPCION', 'NOMBRE_COMPRADOR', 'ESTADO'])  # HEADER
                    writer.writerow([1, id_cuenta, fecha, nombre_compra, monto, descripcion, nombre_comprador, estado])
                else:  # SI EXISTE EL ARCHIVO PERO NO ESTA VACIO
                    id_max = self.max_valor_columna(self.archivo_to_df(self.nombre_archivo_transacciones), "ID")
                    writer.writerow([id_max + 1, id_cuenta, fecha, nombre_compra, monto, descripcion, nombre_comprador, estado])
            elif not self.existe_archivo(self.nombre_archivo_transacciones):  # SI NO EXISTE EL ARCHIVO
                writer.writerow(['ID', 'ID_CUENTA', 'FECHA', 'NOMBRE_COMPRA', 'MONTO', 'DESCRIPCION', 'NOMBRE_COMPRADOR', 'ESTADO'])  # HEADER
                writer.writerow([1, id_cuenta, fecha, nombre_compra, monto, descripcion, nombre_comprador, estado])
            else:
                print("ERROR AL GUARDAR LA TRANSACCION, NO DEBERIA SUCEDER")

    @staticmethod
    def archivo_to_df(nombre_archivo):  # RETORNA EL DF DEl ARCHIVO RECIBIDO
        df = pd.read_csv(nombre_archivo)
        return df

    # TODO: ENCRIPTAR DATOS
    def guarda_cuenta_csv(self, banco, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular):
        # print('deberia guardar la wea: ' + self.banco)
        # print('Banco: ' + str(self.banco.get()) + ', Tipo de cuenta: ' + str(self.tipo_cuenta.get()) + ', Numero de Cuenta: ' + str(self.numero_cuenta.get()) + ', Nombre Titular: ' + str(self.nombre_titular.get()) + ', Apellido Titular: ' + str(self.apellido_titular.get()) + ', Rut: ' + str(self.rut_titular.get()))
        #self.lista_cuentas.append(self)
        with open(self.nombre_archivo_cuentas, mode='a', newline='') as archivo:  # mode='a|w' 'a' PARA NO TRUNCAR EL ARCHIVO Y 'w' PARA TRUNCAR
            writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            if self.existe_archivo(self.nombre_archivo_cuentas):  # SI EXISTE EL ARCHIVO
                if self.file_empty(self.nombre_archivo_cuentas):  # SI EXISTE EL ARCHIVO PERO ESTA VACIO
                    writer.writerow(['ID', 'BANCO', 'TIPO_CUENTA', 'NUMERO_CUENTA', 'NOMBRE_TITULAR', 'APELLIDO_TITULAR', 'RUT_TITULAR'])  # HEADER
                    writer.writerow([1, banco, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular])
                else:  # SI EXISTE EL ARCHIVO PERO NO ESTA VACIO
                    id_max = self.max_valor_columna(self.archivo_to_df(self.nombre_archivo_cuentas), "ID")
                    writer.writerow([id_max + 1, banco, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular])
            elif not self.existe_archivo(self.nombre_archivo_cuentas):  # SI NO EXISTE EL ARCHIVO
                writer.writerow(['ID', 'BANCO', 'TIPO_CUENTA', 'NUMERO_CUENTA', 'NOMBRE_TITULAR', 'APELLIDO_TITULAR', 'RUT_TITULAR'])  # HEADER
                writer.writerow([1, banco, tipo_cuenta, numero_cuenta, nombre_titular, apellido_titular, rut_titular])
            else:
                print("ERROR AL GUARDAR LA CUENTA, NO DEBERIA SUCEDER")

    @staticmethod
    def max_valor_columna(df, columna):
        saved_column = df[columna]
        valor_maximo = saved_column.max()
        print(valor_maximo)
        return valor_maximo

    @staticmethod
    def existe_archivo(archivo):
        file_exists = os.path.isfile(archivo)
        if file_exists:
            return True
        else:
            return False

    @staticmethod
    def file_empty(archivo):
        if os.stat(archivo).st_size == 0:
            return True
        else:
            return False
