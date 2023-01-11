import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import sqlite3
import datetime

class Cliente:
    
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("BASE DE DATOS JOSE COMERCIAL")
        self.ventana1.geometry('2140x1280')
        self.cuaderno1 = ttk.Notebook(self.ventana1)
        self.Agregar_Cliente()
        self.buscar_cliente()
        self.agregar_presupuesto()
        self.datos_de_compra_cliente_bristol()
        self.comision_bristo_porcentaje()
        self.consultar_cuenta_total()
        self.filtrar_cliente_bristo_fecha()
        self.cliente_tes_de_bristol()
        self.view_a_credito()
        self.view_a_contado()
        self.view_total_cobrar()
        self.treview_ventas_del_mes_credito()
        self.treview_ventas_del_mes_contado()
        self.style.configure('BW.TLabel', font=('Arial', 10))
        self.ventana1.configure(bg='Azure')
        self.ventana1.mainloop()
####################################PRIMER PANEL PARA AGREGAR CLIENTE####################################

    def Agregar_Cliente(self):
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="AGREGAR CLIENTE")
        self.labelframe1=ttk.LabelFrame(self.pagina1, text="AGREGAR DATOS") 
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.style = ttk.Style(self.pagina1)
        self.style.theme_use('clam')
        self.label_CI=ttk.Label(self.labelframe1, text="CI:")
        self.label_CI.grid(column=0, row=0, padx=4, pady=4,)
        self.CI_agregar_cliente=tk.StringVar()
        self.entryNombre_Apellido=ttk.Entry(self.labelframe1, textvariable=self.CI_agregar_cliente)
        self.entryNombre_Apellido.grid(column=1, row=0, padx=4, pady=4)
        self.LabelNombre_Apellido=ttk.Label(self.labelframe1, text="NOMBRE Y APELLIDO",style='BW.TLabel')
        self.LabelNombre_Apellido.grid(column=0, row=1, padx=4, pady=4)
        self.nombre_Apellido=tk.StringVar()
        self.entrynumero_tel=ttk.Entry(self.labelframe1, textvariable=self.nombre_Apellido)
        self.entrynumero_tel.grid(column=1, row=1, padx=4, pady=4)
        self.label_tel=ttk.Label(self.labelframe1, text="NRO. TEL: ")
        self.label_tel.grid(column=0, row=2, padx=4, pady=4)
        self.numero_tel=tk.StringVar()
        self.entry_numero_tel=ttk.Entry(self.labelframe1, textvariable=self.numero_tel)
        self.entry_numero_tel.grid(column=1, row=2, padx=4, pady=4)  
        self.cuaderno1.grid(column=0, row=0, padx=10, pady=10)
        self.btn_guardar_cliente=ttk.Button(self.labelframe1, text="GUARDAR", command=self.funcion_para_agregar_cliente)
        self.btn_guardar_cliente.grid(column=1, row=5, padx=4, pady=4)

    def funcion_para_agregar_cliente(self):
        try:
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into usuarios (CI, nombre,numero) values (?,?,?)", ( self.CI_agregar_cliente.get(),
                self.nombre_Apellido.get(),
                self.numero_tel.get()))
            self.conexion.commit()
            self.conexion.close()        
            mb.showinfo(message="Cliente Agregado Correctamente!", title="Exito!")
        except sqlite3.IntegrityError:
            mb.showwarning(message="Cliente con numero CI: {} ya existe!".format(self.CI_agregar_cliente.get()), title="Alerta")
        except sqlite3.OperationalError:
            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")

####################################BUSCAR/CONSULTAR CLIENTE####################################
    def buscar_cliente(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text="BUSCAR CLIENTES")
        self.labelframe2=ttk.LabelFrame(self.pagina2, text="INGRESAR DATOS")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe2, text="CI:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.CI=tk.StringVar()
        self.EntryCI=ttk.Entry(self.labelframe2, textvariable=self.CI)
        self.EntryCI.grid(column=1, row=0, padx=4, pady=4)
        self.label2=ttk.Label(self.labelframe2, text="NOMBRE Y APELLIDO:")        
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.Nombre=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe2, textvariable=self.Nombre, state="readonly")
        self.entrydescripcion.grid(column=1, row=1, padx=4, pady=4)
        self.label3=ttk.Label(self.labelframe2, text="NRO.TELEFONO:")        
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.precio=tk.StringVar()
        self.numero_telefonovar = tk.StringVar()
        self.numero_telefono=ttk.Entry(self.labelframe2, textvariable=self.numero_telefonovar, state="readonly")
        self.numero_telefono.grid(column=1, row=2, padx=4, pady=4)
        self.botony1=ttk.Button(self.labelframe2, text="BUSCAR", command=self.funcion_consultar_datos)
        self.botony1.grid(column=2, row=0, padx=4, pady=4)

    def funcion_consultar_datos(self):
        try:
            self.conexion = sqlite3.connect("xline.db")
            self.cursor = self.conexion.cursor()
            self.cursor.execute("SELECT * FROM usuarios WHERE CI={}".format(self.CI.get()))
            self.all_cartera = self.cursor.fetchall()
            self.all_cartera = list(self.all_cartera) 
            for self.clienteX in self.all_cartera:
                self.Nombre.set(self.clienteX[1])
                self.numero_telefonovar.set(self.clienteX[2])    
            self.conexion.close()
            if self.all_cartera == []:
                mb.showwarning(message="Cliente con numero CI: {} no existe!".format(self.CI.get()), title="Alerta")
            else:
                self.menu_desplegable_de_busqueda()
        except sqlite3.OperationalError:
            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")

    def menu_desplegable_de_busqueda(self):
        self.boton_estado_cuenta=ttk.Button(self.labelframe2, text="ESTADO DE CUENTA", command=self.ver_estado_de_cuenta_fucion)
        self.boton_estado_cuenta.grid(column=2, row=1, padx=4, pady=4)
        self.consultar_cuenta_total()

    def agregar_presupuesto(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="AGREGAR PRESUPUESTO DE CLIENTE")
        self.labelframe3=ttk.LabelFrame(self.pagina3, text="INGRESAR DATOS")
        self.labelframe3.grid(column=0, row=0, padx=5, pady=10)
        self.labelx1=ttk.Label(self.labelframe3, text="CI:")
        self.labelx1.grid(column=0, row=0, padx=4, pady=4)
        self.CI_agregar_prepuesto=tk.StringVar()
        self.EntryCIprepusto=ttk.Entry(self.labelframe3, textvariable=self.CI_agregar_prepuesto)
        self.EntryCIprepusto.grid(column=1, row=0, padx=4, pady=4)
        self.labelx2=ttk.Label(self.labelframe3, text="NOMBRE DE PRODUCTO:")
        self.labelx2.grid(column=0, row=1, padx=4, pady=4)
        self.Nombre_Producto=tk.StringVar()
        self.NombreEntryProducto=ttk.Entry(self.labelframe3, textvariable=self.Nombre_Producto)
        self.NombreEntryProducto.grid(column=1, row=1, padx=4, pady=4)
        self.labelx3=ttk.Label(self.labelframe3, text="MONTO DE CUOTAS:")
        self.labelx3.grid(column=0, row=2, padx=4, pady=4)
        self.monto_cuotas=tk.StringVar()
        self.Entrymontocuotas=ttk.Entry(self.labelframe3, textvariable=self.monto_cuotas)
        self.Entrymontocuotas.grid(column=1, row=2, padx=4, pady=4)
        self.labelx4=ttk.Label(self.labelframe3, text="CANTIDAD DE CUOTAS:")
        self.labelx4.grid(column=0, row=3, padx=4, pady=4)
        self.CantidadCuotas=tk.StringVar()
        self.EntryCuotaCantidad=ttk.Entry(self.labelframe3, textvariable=self.CantidadCuotas)
        self.EntryCuotaCantidad.grid(column=1, row=3, padx=4, pady=4)
        self.labelx5=ttk.Label(self.labelframe3, text="CODIGO DE PRODUCTO:")
        self.labelx5.grid(column=0, row=4, padx=4, pady=4)
        self.CodigoProducto=tk.StringVar()
        self.EntryCodigoProducto=ttk.Entry(self.labelframe3, textvariable=self.CodigoProducto)
        self.EntryCodigoProducto.grid(column=1, row=4, padx=4, pady=4)
        self.boton3=ttk.Button(self.labelframe3, text="  AGREGAR  ", command=self.agregar_prepuesto_cliente)
        self.boton3.grid(column=4, row=0, padx=4, pady=4)

    def menu_desplegable_de_busqueda(self):
        self.botonx1=ttk.Button(self.labelframe2, text="ESTADO DE CUENTA", command=self.ver_estado_de_cuenta_fucion)
        self.botonx1.grid(column=2, row=1, padx=4, pady=4)
        self.consultar_cuenta_total()

    def ver_estado_de_cuenta_fucion(self): #FUNCION PARA VER EL ESTADO DE CUENTA DEL CLIENTE CON CUOTAS, PRESUPUESTO Y DEMAS 
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM cuenta WHERE CI={}".format(self.CI.get()))
        self.todos_los_productos = self.cursor.fetchall()
        self.Lista_productos = []
        for self.productos_x in self.todos_los_productos:
            self.Lista_productos.append(self.productos_x) 
        self.conexion.close()
        self.columns = ('CI', 'Producto', 'Monto_de_cuotas','cantidad_de_cuotas','Codigo_de_producto','Fecha_de_adquision','Presupuesto_total')
        self.tree = ttk.Treeview(self.pagina2, height=10,columns=self.columns, show='headings')
        self.tree.heading('CI', text='CI: ')
        self.tree.heading('Producto', text='PRODUCTO:')
        self.tree.heading('Monto_de_cuotas', text='MONTO DE CUOTAS:')
        self.tree.heading('cantidad_de_cuotas', text='CUOTAS RESTANTES: ')
        self.tree.heading('Codigo_de_producto', text='CODIGO DE PRODUCTO: ')
        self.tree.heading('Fecha_de_adquision', text='FECHA DE ADQUISICION: ')
        self.tree.heading('Presupuesto_total', text='PRESUPUESTO TOTAL: ')
        self.tree.column('#1', width=40, anchor='c')
        self.contacts = []
        self.prepuesto_total_del_cliente = []
        for self.dato_clientex in self.Lista_productos:
            self.prepuesto_total_del_cliente.append(f'{self.dato_clientex[6]}')
            self.contacts.append((f'{self.dato_clientex[0]}',
                f'{self.dato_clientex[1]}',
                f'{self.dato_clientex[2]}',
                f'{self.dato_clientex[3]}',
                f'{self.dato_clientex[4]}',
                f'{self.dato_clientex[5]}',
                f'{self.dato_clientex[6]}'))
        self.menu_de_deuda_total()
        self.prepuesto_lista_total= list(map(int, self.prepuesto_total_del_cliente))
        self.prepuesto_int_total = 0
        for self.presupustox in self.prepuesto_lista_total:
            self.prepuesto_int_total =  self.prepuesto_int_total + self.presupustox
        self.prepuesto_int_total1 = ("{:,}".format(self.prepuesto_int_total))
        self.producto_total_prepuesto.set(self.prepuesto_int_total1)
        for self.contact in self.contacts:
            if int(self.contact[6]) <= 0:
                pass
            else:
                self.tree.insert('', tk.END, values=self.contact)
        self.tree.bind('<<TreeviewSelect>>',self.menu_boton_disponible) # UNA VEZ SELECIONADO ESTE COMMAND SE HABILITA EL MENO PARA PAGO
        self.tree.grid(row=6, column=0, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self.pagina2, orient=tk.VERTICAL, command=None)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=1, sticky='ns')
        self.label_treview=ttk.Label(self.labelframe2, text="OPCIONES DE PAGO")        
        self.label_treview.grid(column=2, row=2, padx=4, pady=4)
        self.pago_prepuesto_label4=ttk.Label(self.labelframe2, text="MONTO DE PAGO:")        
        self.pago_prepuesto_label4.grid(column=0, row=3, padx=4, pady=4)
        self.entry_disable=ttk.Entry(self.labelframe2, state="disabled", textvariable=None)
        self.entry_disable.grid(column=1, row=3, padx=4, pady=4)
        self.btn_presupuesto_pago=ttk.Button(self.labelframe2, text="PAGAR AL CONTADO", command=None)
        self.btn_presupuesto_pago.grid(column=2, row=3, padx=4, pady=4)
        self.btn_presupuesto_pago.config(state = 'disabled')
        self.btn_presupuesto_pago1=ttk.Button(self.labelframe2, text="    PAGAR A CUOTAS  ", command=None)
        self.btn_presupuesto_pago1.grid(column=2, row=4, padx=4, pady=4)
        self.btn_presupuesto_pago1.config(state = 'disabled')
        self.btn_presupuesto_pago2=ttk.Button(self.labelframe2, text="      VER HISTORIAL      ", command=None)
        self.btn_presupuesto_pago2.grid(column=2, row=5, padx=4, pady=4)
        self.btn_presupuesto_pago2.config(state = 'disabled')
        self.historial_pagos_view()

    def menu_boton_disponible(self,event):
        self.pago_prepuestovar = tk.IntVar()
        self.pago_prepuesto_entry2=ttk.Entry(self.labelframe2, textvariable=self.pago_prepuestovar)
        self.pago_prepuesto_entry2.grid(column=1, row=3, padx=4, pady=4)
        self.btn_presupuesto_pago=ttk.Button(self.labelframe2, text="PAGAR AL CONTADO", command=self.pagar_prepuesto_funcion_contado)
        self.btn_presupuesto_pago.grid(column=2, row=3, padx=4, pady=4)
        self.btn_presupuesto_pago1=ttk.Button(self.labelframe2, text="    PAGAR A CUOTAS  ", command=self.pagar_por_cuotas)
        self.btn_presupuesto_pago1.grid(column=2, row=4, padx=4, pady=4)
        self.btn_presupuesto_pago2=ttk.Button(self.labelframe2, text="      VER HISTORIAL      ", command=self.historial_pagos_view)
        self.btn_presupuesto_pago2.grid(column=2, row=5, padx=4, pady=4)

    def menu_de_deuda_total(self):
        self.producto_totaleslabel=ttk.Label(self.labelframe2, text="DEUDA TOTAL:")        
        self.producto_totaleslabel.grid(column=0, row=4, padx=4, pady=4)
        self.producto_total_prepuesto = tk.IntVar()
        self.producto_totalesentry=ttk.Entry(self.labelframe2, textvariable=self.producto_total_prepuesto)
        self.producto_totalesentry.grid(column=1, row=4, padx=4, pady=4)
#################################### MENU DE PAGO ####################################
#################################### PAGO AL CONTADO ####################################
    def pagar_prepuesto_funcion_contado(self): 
        if mb.askyesnocancel(message="¿Estas seguro que deseas pagar prepuesto al contado?", title="Alerta!") == True:
            try:
                self.valores_de_productos1 = self.tree.item(self.tree.selection())['values']
                self.nombre_de_producto_final = self.valores_de_productos1[1]
                self.cantidad_cuotas_actual_contado = int(self.valores_de_productos1[3])
                self.codigo_final_de_presupuesto = int(self.valores_de_productos1[4])
                self.prepuesto_total_a_pagar = (self.valores_de_productos1[6] - self.pago_prepuestovar.get()) # SE RESTA EL MONTO DE PAGO AL PREPUESTO TOTAL
                #CONEXION CON SQLITE
                self.conexion = sqlite3.connect('xline.db')
                self.conexion.execute('UPDATE cuenta SET cantidad_cuotas=0,presupuesto_total={} WHERE codigo_producto={}'.format(int(self.prepuesto_total_a_pagar),
                    self.codigo_final_de_presupuesto))
                self.conexion.commit()
                self.conexion.close()
                mb.showinfo(message="Pago Exitoso! Presupuesto estante: {:,}".format(self.prepuesto_total_a_pagar), title="Alerta") #REALIZA PAGO
                #############■GUARDA HISTORIAL DE PAGO#################
                try:
                    self.date_pago_contado = datetime.datetime.now()
                    self.date_pago_contado = str(self.date_pago_contado)[:19]
                    self.conexion = sqlite3.connect("xline.db")
                    self.valores_de_productos2 = self.tree.item(self.tree.selection())['values']
                    self.codigo_final_de_producto = int(self.valores_de_productos2[4])
                    self.cantidad_cuotas_actual_contado = int(self.valores_de_productos2[3])
                    self.producto_actual_contado = self.valores_de_productos2[1]
                    self.cursor = self.conexion.cursor()
                    self.monto_abonado_var = "{:,}".format(self.pago_prepuestovar.get())
                    self.cursor.execute("INSERT into historial_pagos (fecha_pago, CI_cliente,Nombre_cliente,codigo_producto,producto,Cantidad_cuotas,monto_abonado) VALUES (?,?,?,?,?,?,?)", (self.date_pago_contado,
                        self.CI.get(),
                        self.Nombre.get(),
                        self.codigo_final_de_producto,
                        self.producto_actual_contado,
                        self.cantidad_cuotas_actual_contado,
                        self.monto_abonado_var))
                    self.conexion.commit()
                    self.conexion.close()
                    self.ver_estado_de_cuenta_fucion()
                    self.historial_pagos_view()
                except IndexError:
                    pass
            except sqlite3.OperationalError:
                mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor cirre el programa y vuelva a intentarlo", title="Alerta")
        else:
            pass

#################################### PAGO A CUOTAS ####################################
    def pagar_por_cuotas(self):
        try:
            if mb.askyesnocancel(message="¿Deseas pagar por cuota?", title="Opciones!") == True:
                try:
                    self.valores_de_productos0 = self.tree.item(self.tree.selection())['values']
                    self.codigo_final_de_producto = int(self.valores_de_productos0[4])
                    self.cantidad_cuotas_actual = int(self.valores_de_productos0[3])
                    self.Monto_cuotas_actual = int(self.valores_de_productos0[2])
                    self.producto_actual = str(self.valores_de_productos0[1])
                    self.cantidad_cuotas_actual = self.cantidad_cuotas_actual -1
                    self.monto_total_actual = self.Monto_cuotas_actual * self.cantidad_cuotas_actual
                except IndexError:
                    pass
                if self.monto_total_actual >= 0:
                    if mb.askyesnocancel(message="¿Estas seguro que deseas pagar la cuota?", title="Alerta!") == True:
                        try:
                            self.conexion = sqlite3.connect('xline.db')
                            self.conexion.execute('UPDATE cuenta SET cantidad_cuotas={}, presupuesto_total={} WHERE codigo_producto={}'.format(self.cantidad_cuotas_actual,
                                int(self.monto_total_actual),
                                self.codigo_final_de_producto))
                            self.conexion.commit()
                            self.conexion.close()
                            mb.showinfo(message="Cuota Pagada!", title="Alerta")
                            try:
                                self.Monto_cuotas_actual = "{:,}".format(self.Monto_cuotas_actual) # AGREGAR FORMATO FORMATO A LOS NUMEROS
                                self.date_cuotas = datetime.datetime.now()
                                self.date_cuotas = str(self.date_cuotas)[:19]
                                self.conexion = sqlite3.connect("xline.db")
                                self.cursor = self.conexion.cursor()
                                self.cursor.execute("INSERT into historial_pagos (fecha_pago, CI_cliente,Nombre_cliente,codigo_producto,producto,Cantidad_cuotas,monto_abonado) VALUES (?,?,?,?,?,?,?)", (self.date_cuotas,
                                    self.CI.get(),
                                    self.Nombre.get(),
                                    self.codigo_final_de_producto,
                                    self.producto_actual,
                                    self.cantidad_cuotas_actual,
                                    self.Monto_cuotas_actual))
                                self.conexion.commit()
                                self.conexion.close()
                                self.ver_estado_de_cuenta_fucion()
                                self.historial_pagos_view()
                            except AttributeError:
                                pass
                        except sqlite3.OperationalError:
                            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")
                    else:
                        mb.showinfo(message="Pago de cuota cancelado!", title="Alerta")
                elif self.monto_total_actual <= 0:
                    mb.showwarning(message="No disponible para este cliente, intente pagar por prepuesto!", title="Alerta")
            else:
                pass
        except IndexError:
            pass

#################################### MENU DE HISTARIAL DE PAGO ####################################
    def historial_pagos_view(self):
        try:
            self.valores_de_productos_historial = self.tree.item(self.tree.selection())['values']
            self.codigo_final_de_producto_historial = int(self.valores_de_productos_historial[4])
            import sqlite3
            self.conexion = sqlite3.connect("xline.db")
            self.cursor = self.conexion.cursor()
            self.cursor.execute("SELECT * FROM historial_pagos WHERE codigo_producto={}".format(self.codigo_final_de_producto_historial))
            self.todos_los_productos_historial = self.cursor.fetchall()
            self.Lista_productos_historial = []
            for self.productos_x_historial in self.todos_los_productos_historial:
                self.Lista_productos_historial.append(self.productos_x_historial) 
            self.conexion.close()
            self.columns_historial = ('FECHA_HISTORIAL', 'CI:', 'NOMBRE_DE_CLIENTE','CODIGO_PRODUCTO','NOMBRE_PRODUCTO','CANTIDAD_DE_CUOTAS','MOTO_CUOTAS_ABONADO')
            self.tree_historial = ttk.Treeview(self.pagina2, height=10,columns=self.columns_historial, show='headings')
            # define headings
            self.tree_historial.heading('FECHA_HISTORIAL', text='FECHA DE PAGO: ')
            self.tree_historial.heading('CI:', text='CI:')
            self.tree_historial.heading('NOMBRE_DE_CLIENTE', text='NOMBRE DE CLIENTE:')
            self.tree_historial.heading('CODIGO_PRODUCTO', text='CODIGO DE PRODUCTO: ')
            self.tree_historial.heading('NOMBRE_PRODUCTO', text='NOMBRE DE PRODUCTO: ')
            self.tree_historial.heading('CANTIDAD_DE_CUOTAS', text='CUOTAS RESTANTE: ')
            self.tree_historial.heading('MOTO_CUOTAS_ABONADO', text='MONTO ABONADO: ')
            self.tree_historial.column('#1', width=40, anchor='c')
            self.contacts_historial = []
            for self.n_historial in self.Lista_productos_historial:
                self.contacts_historial.append((f'{self.n_historial[0]}',
                    f'{self.n_historial[1]}',
                    f'{self.n_historial[2]}',
                    f'{self.n_historial[3]}',
                    f'{self.n_historial[4]}',
                    f'{self.n_historial[5]}',
                    f'{self.n_historial[6]}'))
            for self.contact_historial in self.contacts_historial:
                self.tree_historial.insert('', tk.END, values=self.contact_historial)
            self.tree_historial.bind('<<TreeviewSelect>>')
            self.tree_historial.grid(row=8, column=0, sticky='nsew')
            self.scrollbar_historial = ttk.Scrollbar(self.pagina2, orient=tk.VERTICAL, command=None)
            self.tree_historial.configure(yscroll=self.scrollbar_historial.set)
            self.scrollbar_historial.grid(row=8, column=1, sticky='ns')
        except IndexError:
            pass

#################################### SECCION PARA AGREGAR PREPUESTO####################################
    def agregar_prepuesto_cliente(self):
        try:
            self.PRESUPUESTO = int(self.CantidadCuotas.get()) * int(self.monto_cuotas.get())
            self.fecha_prepuesto= datetime.datetime.now()
            self.fecha_prepuesto = str(self.fecha_prepuesto)[:19]
        except ValueError:
            mb.showwarning(message="Completar todos los campos", title="Alerta")
        import sqlite3
        try:
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into cuenta (CI, producto,monto_cuotas,codigo_producto,cantidad_cuotas,fecha_adquisicion,presupuesto_total) values (?,?,?,?,?,?,?)", (self.CI_agregar_prepuesto.get(),
                self.Nombre_Producto.get(),
                self.monto_cuotas.get(),
                self.CodigoProducto.get(),
                self.CantidadCuotas.get(),
                self.fecha_prepuesto,
                self.PRESUPUESTO))
            self.conexion.commit()
            self.conexion.close()        
            mb.showinfo(message="Presupuesto agregado Correctamente!", title="Exito!")
        except sqlite3.IntegrityError:
            mb.showwarning(message="Producto con codigo: {} ya existe!".format(self.CodigoProducto.get()), title="Alerta")
        except sqlite3.OperationalError:
            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")

    #FUNCIONES DE BRISTOL
    def datos_de_compra_cliente_bristol(self):
        self.pagina4 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina4, text="AGREGAR CLIENTE BRISTOL")
        self.labelframe4=ttk.LabelFrame(self.pagina4, text="INGRESA PRODUCTO Y PREPUESTO")
        self.labelframe4.grid(column=0, row=0, padx=5, pady=10)
        self.ETIQUETA=ttk.Label(self.labelframe4, text="INGRESA DATOS DE LA COMPRA")
        self.ETIQUETA.grid(column=1, row=0, padx=4, pady=4)
        self.bristol1=ttk.Label(self.labelframe4, text="CI:")
        self.bristol1.grid(column=0, row=1, padx=4, pady=4)
        self.bristol_ci=tk.StringVar()
        self.entrycibristol=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.bristol_ci)
        self.entrycibristol.grid(column=1, row=1, padx=4, pady=4)

        self.bristol2=ttk.Label(self.labelframe4, text="NOMBRE Y APELLIDO:")
        self.bristol2.grid(column=0, row=2, padx=4, pady=4)
        self.bristol_nombreyapellido=tk.StringVar()
        self.entrybristonombre=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.bristol_nombreyapellido)
        self.entrybristonombre.grid(column=1, row=2, padx=4, pady=4)

        self.bristol3=ttk.Label(self.labelframe4, text="NRO. TELEFONO:")
        self.bristol3.grid(column=0, row=3, padx=4, pady=4)
        self.tel_bristol=tk.StringVar()
        self.entry_telefono_bristol=ttk.Entry(self.labelframe4, text="Clear text", textvariable=self.tel_bristol)
        self.entry_telefono_bristol.grid(column=1, row=3, padx=4, pady=4)

        self.bristol4=ttk.Label(self.labelframe4, text="PRODUCTO:")
        self.bristol4.grid(column=0, row=4, padx=4, pady=4)
        self.producto_bristol=tk.StringVar()
        self.entry_producto_bristol=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.producto_bristol)
        self.entry_producto_bristol.grid(column=1, row=4, padx=4, pady=4)

        self.bristol5=ttk.Label(self.labelframe4, text="FECHA DE ADQUISICION:")
        self.bristol5.grid(column=0, row=5, padx=4, pady=4)
        self.fecha_bristol=tk.StringVar()
        self.entry_fecha_bristol=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.fecha_bristol)
        self.entry_fecha_bristol.grid(column=1, row=5, padx=4, pady=4)
        self.botonbristol1=ttk.Button(self.labelframe4, text="AGREGAR", command=self.agregar_bristo_cliente)
        self.botonbristol1.grid(column=4, row=1, padx=4, pady=4)
        self.botonbristol2=ttk.Button(self.labelframe4, text="VER CLIENTE", command=self.consultar_bristo_funcion)
        self.botonbristol2.grid(column=4, row=2, padx=4, pady=4)
        self.botonbristol3=ttk.Button(self.labelframe4, text="LIMPIAR", command=self.filtrar_cliente_bristo_fecha)
        self.botonbristol3.grid(column=4, row=3, padx=4, pady=4)
        self.botonbristol4=ttk.Button(self.labelframe4, text="VER TODOS", command=self.treeview_todos_los_clientes)
        self.botonbristol4.grid(column=4, row=4, padx=4, pady=4)

    def escribaFecha(self, event):
        if event.char.isdigit():
            self.texto = self.entryFecha.get()
            self.letras = 0
            for self.i in self.texto:
                self.letras +=1
            if self.letras == 2:
                self.entryFecha.insert(2,"/")
            elif self.letras == 5:
                self.entryFecha.insert(5,"/")
        else:
            return "break"

    def escribaFecha_1(self, event):
        if event.char.isdigit():
            self.texto_1 = self.entryFecha_1.get()
            self.letras_1 = 0
            for self.i_1 in self.texto_1:
                self.letras_1 +=1
            if self.letras_1 == 2:
                self.entryFecha_1.insert(2,"/")
            elif self.letras_1 == 5:
                self.entryFecha_1.insert(5,"/")
        else:
            return "break"

    def filtrar_cliente_bristo_fecha(self):
        self.LABEL_FILTRO=ttk.Label(self.labelframe4, text="FILTAR CLIENTES POR FECHA")
        self.LABEL_FILTRO.grid(column=7, row=2, padx=4, pady=4)
        self.fecha1 = tk.StringVar()
        self.entryFecha = tk.Entry(self.labelframe4, textvariable=self.fecha1)
        self.entryFecha.grid(row = 3, column = 7, pady = 10, padx = 10)
        self.entryFecha.bind("<Key>", self.escribaFecha)
        self.entryFecha.bind("<BackSpace>", lambda _:self.entryFecha.delete(tk.END))
        self.fecha2 = tk.StringVar()
        self.entryFecha_1 = tk.Entry(self.labelframe4, textvariable=self.fecha2)
        self.entryFecha_1.grid(row = 4, column = 7, pady = 10, padx = 10)

        self.fecha3 = tk.StringVar()
        self.entryFecha_3 = tk.Entry(self.labelframe4, textvariable=self.fecha3)
        self.entryFecha_3.grid(row = 5, column = 7, pady = 10, padx = 10)

        self.entryFecha_1.bind("<Key>", self.escribaFecha_1)
        self.entryFecha_1.bind("<BackSpace>", lambda _:self.entryFecha_1.delete(tk.END))
        self.columns_BRISTOL = ('CI_BRISTOL_CLIENTE', 'NOMBRE_APELLIDO', 'NUMERO_DE_TELEFONO','PRODUCTO','FECHA','OBSERVACION_TIP',)
        self.tree_bristol = ttk.Treeview(self.pagina4, height=5,columns=self.columns_BRISTOL, show='headings')
        # define headings
        self.tree_bristol.heading('CI_BRISTOL_CLIENTE', text='NRO DE CI: ')
        self.tree_bristol.heading('NOMBRE_APELLIDO', text='NOMBRE Y APELLIDO:')
        self.tree_bristol.heading('NUMERO_DE_TELEFONO', text='NRO DE TELEFONO:')
        self.tree_bristol.heading('PRODUCTO', text='PRODUCTO ADQUIRIDO: ')
        self.tree_bristol.heading('FECHA', text='FECHA DE ADQUISION: ')
        self.tree_bristol.heading('OBSERVACION_TIP', text='TIPO DE CLIENTE: ')
        self.tree_bristol.column('#1', width=100, anchor='c')

    def treeview_todos_los_clientes(self):
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM presupuesto_bristol_cliente")
        self.todos_los_clientes_bristol = self.cursor.fetchall()
        self.lista_bristol_cliente = []
        for self.clintes_x in self.todos_los_clientes_bristol:
            self.lista_bristol_cliente.append(self.clintes_x) 
        self.conexion.close()
        self.columns_BRISTOL = ('CI_BRISTOL_CLIENTE', 'NOMBRE_APELLIDO', 'NUMERO_DE_TELEFONO','PRODUCTO','FECHA')
        self.tree_bristol = ttk.Treeview(self.pagina4, height=5,columns=self.columns_BRISTOL, show='headings')

        # define headings
        self.tree_bristol.heading('CI_BRISTOL_CLIENTE', text='NRO DE CI: ')
        self.tree_bristol.heading('NOMBRE_APELLIDO', text='NOMBRE Y APELLIDO:')
        self.tree_bristol.heading('NUMERO_DE_TELEFONO', text='NRO DE TELEFONO:')
        self.tree_bristol.heading('PRODUCTO', text='PRODUCTO ADQUIRIDO: ')
        self.tree_bristol.heading('FECHA', text='FECHA DE ADQUISION: ')
        self.tree_bristol.column('#1', width=100, anchor='c')
        self.clientes_bristol_list = []
        for self.cliene_xbristol in self.todos_los_clientes_bristol:
            self.clientes_bristol_list.append((f'{self.cliene_xbristol[0]}',
                f'{self.cliene_xbristol[1]}',
                f'{self.cliene_xbristol[2]}',
                f'{self.cliene_xbristol[3]}',
                f'{self.cliene_xbristol[4]}'))
        for self.clientes_list in self.clientes_bristol_list:
            self.tree_bristol.insert('', tk.END, values=self.clientes_list)
        self.tree_bristol.bind('<<TreeviewSelect>>')
        self.tree_bristol.grid(row=8, column=0, sticky='nsew')
        self.scrollbar_bristol = ttk.Scrollbar(self.pagina4, orient=tk.VERTICAL, command=None)
        self.tree_bristol.configure(yscroll=self.scrollbar_bristol.set)
        self.scrollbar_bristol.grid(row=8, column=1, sticky='ns')



    def agregar_bristo_cliente(self):
        try:
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into presupuesto_bristol_cliente (CI_BRISTOL,NOMBRE_APELLIDO_BRISTOL,NUMERO_TELEFONO,PRODUCTO,FECHA) values (?,?,?,?,?,?)", ( self.bristol_ci.get(),
                self.bristol_nombreyapellido.get(),
                self.tel_bristol.get(),
                self.producto_bristol.get(),
                self.fecha_bristol.get()))
            self.conexion.commit()
            self.conexion.close()
            self.clear_text()
            mb.showinfo(message="Cliente Agregado Correctamente!", title="Exito!")
        except sqlite3.IntegrityError:
            mb.showwarning(message="Cliente ya existe", title="Error!")
        except sqlite3.OperationalError:
            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")

    def cliente_tes_de_bristol(self):
        self.ETIQUETA=ttk.Label(self.labelframe4, text="INGRESA DATOS DE DEL CLIENTE")
        self.ETIQUETA.grid(column=6, row=0, padx=4, pady=4)

        self.labelbristolci=ttk.Label(self.labelframe4, text="CI:")
        self.labelbristolci.grid(column=5, row=1, padx=4, pady=4)
        self.ci_datos=tk.StringVar()
        self.entry_ci_bristol=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.ci_datos)
        self.entry_ci_bristol.grid(column=6, row=1, padx=4, pady=4)

        self.labelNombreApellido=ttk.Label(self.labelframe4, text="NOMBRE Y APELLIDO:")
        self.labelNombreApellido.grid(column=5, row=2, padx=4, pady=4)
        self.nombreApellidobristolsa=tk.StringVar()
        self.entrylabelNombreApellido=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.nombreApellidobristolsa)
        self.entrylabelNombreApellido.grid(column=6, row=2, padx=4, pady=4)

        self.NRO_TELEFONO_LABEL=ttk.Label(self.labelframe4, text="NRO. TELEFONO")
        self.NRO_TELEFONO_LABEL.grid(column=5, row=3, padx=4, pady=4)
        self.NRO_TELEFONO_VAR=tk.StringVar()
        self.ENTRY_NRO_TELEFONO_VAR=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.NRO_TELEFONO_VAR)
        self.ENTRY_NRO_TELEFONO_VAR.grid(column=6, row=3, padx=4, pady=4)


        self.TIPO_LABEL=ttk.Label(self.labelframe4, text="TIPO DE CLIENTE")
        self.TIPO_LABEL.grid(column=5, row=4, padx=4, pady=4)
        self.TIPO_CLIENTE_VAR=tk.StringVar()
        self.ENTRY_TIPO_CLIENTE=ttk.Entry(self.labelframe4,text="Clear text", textvariable=self.TIPO_CLIENTE_VAR)
        self.ENTRY_TIPO_CLIENTE.grid(column=6, row=4, padx=4, pady=4)

        self.guardar_cliente_blistol_btn=ttk.Button(self.labelframe4, text="GUARDAR", command=self.agregar_bristo_cliente_DATOS)
        self.guardar_cliente_blistol_btn.grid(column=6, row=5, padx=4, pady=4)

        self.btn_3 = ttk.Button(self.labelframe4, text="BUSCAR CLIENTE", command=None)
        self.btn_3.grid(column=7, row=1, padx=4, pady=4)


    def agregar_bristo_cliente_DATOS(self):
        try:
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into cliente_bristol (CI_BRISTOL_DATOS,NOMBRE_APELLIDO_BRISTOL2,NRO_CELULAR,OBSERVACION) values (?,?,?,?)", ( self.ci_datos.get(),
                self.nombreApellidobristolsa.get(),
                self.NRO_TELEFONO_VAR.get(),
                self.TIPO_CLIENTE_VAR.get()))
            self.conexion.commit()
            self.conexion.close()
            self.clear_text()
            mb.showinfo(message="Cliente Agregado Correctamente!", title="Exito!")
        except sqlite3.IntegrityError:
            mb.showwarning(message="Cliente ya existe", title="Error!")
        except sqlite3.OperationalError:
            mb.showwarning(message="Error base de datos posiblemente bloqueado, por favor vuelva a intentarlo", title="Alerta")
    def consultar_bristo_funcion(self):
        import sqlite3
        try:

            self.conexion = sqlite3.connect("xline.db")
            self.cursor = self.conexion.cursor()
            self.cursor.execute("SELECT * FROM presupuesto_bristol_cliente WHERE CI_BRISTOL={}".format(self.bristol_ci.get()))
            self.lista_clientes_bristol = self.cursor.fetchall()
            self.lista_clientes_bristol = list(self.lista_clientes_bristol)
            if self.lista_clientes_bristol == []:
                mb.showwarning(message="Cliente no existe", title="Alerta")
            else:
                for self.bristol_client in self.lista_clientes_bristol:
                    self.bristol_nombreyapellido.set(self.bristol_client[1])
                    self.tel_bristol.set(self.bristol_client[2]) 
                    self.producto_bristol.set(self.bristol_client[3]) 
                    self.fecha_bristol.set(self.bristol_client[4])  
                self.conexion.close()
        except sqlite3.OperationalError:
            mb.showinfo(message="Completar campo para consultar", title="Alerta")


#FUNCIONES  DE CALULO DE PORCENTAJE 
    def comision_bristo_porcentaje(self):
        self.pagina5 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina5, text="CALCULAR COMISION EN BRISTOL")
        self.labelframe5=ttk.LabelFrame(self.pagina5, text="Ingresa datos")
        self.labelframe5.grid(column=0, row=0, padx=5, pady=10)
        self.labelguardar=ttk.Label(self.labelframe5, text="GUARDAR VENTAS DEL DIA")
        self.labelguardar.grid(column=7, row=0, padx=4, pady=4)
        self.Nombre_venta_dia=ttk.Label(self.labelframe5, text="NOMBRE Y APELLIDO")
        self.Nombre_venta_dia.grid(column=6, row=1, padx=4, pady=4)
        self.Venta_dia_nombre = tk.StringVar()
        self.entry_Venta_del_dia=ttk.Entry(self.labelframe5,text="Clear text", textvariable=self.Venta_dia_nombre)
        self.entry_Venta_del_dia.grid(column=7, row=1, padx=4, pady=4)
        self.ci_label=ttk.Label(self.labelframe5, text="NUMERO CI")
        self.ci_label.grid(column=6, row=2, padx=4, pady=4)
        self.ci_dia = tk.StringVar()
        self.entry_ci=ttk.Entry(self.labelframe5,text="Clear text", textvariable=self.ci_dia)
        self.entry_ci.grid(column=7, row=2, padx=4, pady=4)
        self.producto_dia_label=ttk.Label(self.labelframe5, text="PRODUCTO")
        self.producto_dia_label.grid(column=6, row=3, padx=4, pady=4)
        self.producto_diavar = tk.StringVar()
        self.entryproducto_diavar=ttk.Entry(self.labelframe5,text="Clear text", textvariable=self.producto_diavar)
        self.entryproducto_diavar.grid(column=7, row=3, padx=4, pady=4)
        self.monto_dia_label=ttk.Label(self.labelframe5, text="MONTO DEL DIA")
        self.monto_dia_label.grid(column=6, row=4, padx=4, pady=4)
        self.monto_dia = tk.StringVar()
        self.entrymonto_dia=ttk.Entry(self.labelframe5,text="Clear text", textvariable=self.monto_dia)
        self.entrymonto_dia.grid(column=7, row=4, padx=4, pady=4)
        self.btn_credito=ttk.Button(self.labelframe5, text="GUARDAR", command=self.guardar_menu_despliege)
        self.btn_credito.grid(column=8, row=1, padx=4, pady=4)

        self.label_tota_credito=ttk.Label(self.labelframe5, text="TOTAL CREDITO VENDIDO:")
        self.label_tota_credito.grid(column=0, row=0, padx=4, pady=4)
        self.var_total_credito = tk.StringVar()
        self.entry_total_credito=ttk.Entry(self.labelframe5,state='readonly', textvariable=self.var_total_credito)
        self.entry_total_credito.grid(column=1, row=0, padx=4, pady=4)
        self.label_credito_cobrar=ttk.Label(self.labelframe5, text="TOTAL A COBRAR A CREDITO:")
        self.label_credito_cobrar.grid(column=0, row=1, padx=4, pady=4)
        self.var_credito_cobrar = tk.StringVar()
        self.entry_credito_cobrar=ttk.Entry(self.labelframe5,state='readonly', textvariable=self.var_credito_cobrar)
        self.entry_credito_cobrar.grid(column=1, row=1, padx=4, pady=4)
        self.label_tota_credito=ttk.Label(self.labelframe5, text="TOTAL CONTADO:")
        self.label_tota_credito.grid(column=0, row=2, padx=4, pady=4)
        self.var_total_contado = tk.StringVar()
        self.entry_total_contado=ttk.Entry(self.labelframe5,state='readonly', textvariable=self.var_total_contado)
        self.entry_total_contado.grid(column=1, row=2, padx=4, pady=4)
        self.label_tota_contado=ttk.Label(self.labelframe5, text="TOTAL A COBRAR AL CONTADO:")
        self.label_tota_contado.grid(column=0, row=3, padx=4, pady=4)
        self.total_a_cobrar_contado = tk.StringVar()
        self.entry_total_contado=ttk.Entry(self.labelframe5,state='readonly', textvariable=self.total_a_cobrar_contado)
        self.entry_total_contado.grid(column=1, row=3, padx=4, pady=4)
        self.label_total_ips=ttk.Label(self.labelframe5, text="TOTAL A COBRAR CON IPS:")
        self.label_total_ips.grid(column=0, row=4, padx=4, pady=4)
        self.var_total_ips = tk.StringVar()
        self.entry_total_ips=ttk.Entry(self.labelframe5,state='readonly', textvariable=self.var_total_ips)
        self.entry_total_ips.grid(column=1, row=4, padx=4, pady=4)
        
    def clear_text(self):
        self.entrycibristol.delete(0, 'end')
        self.entrybristonombre.delete(0, 'end')
        self.entry_telefono_bristol.delete(0, 'end')
        self.entry_producto_bristol.delete(0, 'end')
        self.entry_fecha_bristol.delete(0, 'end')
        
        self.entry_Venta_del_dia.delete(0, 'end')
        self.entry_ci.delete(0, 'end')
        self.entryproducto_diavar.delete(0, 'end')
        self.entrymonto_dia.delete(0, 'end')
    def guardar_menu_despliege(self):
        self.btn_credito_guardar=ttk.Button(self.labelframe5, text="CREDITO", command=self.guardar_ventas_credito)
        self.btn_credito_guardar.grid(column=8, row=2, padx=4, pady=4)
        self.btn_credito_guardar1=ttk.Button(self.labelframe5, text="CONTADO", command=self.guardar_ventas_contado)
        self.btn_credito_guardar1.grid(column=8, row=3, padx=4, pady=4)
        self.borrar=ttk.Button(self.labelframe5, text="BORRAR TODO", command=self.delete_ventas)
        self.borrar.grid(column=6, row=5, padx=4, pady=4)

    def guardar_ventas_credito(self):
        if mb.askyesnocancel(message="¿Deseas agregar a venta de credito?", title="Opciones!") == True:
            self.date_dia = datetime.datetime.now()
            self.date_dia = str(self.date_dia)[:19]
            self.date_BORRAR = datetime.datetime.now()
            self.date_BORRAR = str(self.date_BORRAR)[20:26]
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into venta_dia_credito (NOMBRE_DIA,CI_DIA,PRODUCTO_DIA,MONTO_DIA,FECHA_DIA,BORRAR) values (?,?,?,?,?,?)", ( self.Venta_dia_nombre.get(),
                self.ci_dia.get(),
                self.producto_diavar.get(),
                self.monto_dia.get(),
                self.date_dia,
                self.date_BORRAR))
            self.conexion.commit()
            self.conexion.close() 
            mb.showinfo(message="Venta guardado correctamente", title="Exito!")
            self.view_a_credito()
            self.view_a_contado()
            self.view_total_cobrar()
            self.clear_text()
            self.treview_ventas_del_mes_credito()
        else:
            mb.showinfo(message="Operacion cancelado",title="Cancelado")
    def guardar_ventas_contado(self):
        if mb.askyesnocancel(message="¿Deseas agregar a venta de credito?", title="Opciones!") == True:
            self.date_diac = datetime.datetime.now()
            self.date_diac = str(self.date_diac)[:19]
            self.date_BORRAR_contado = datetime.datetime.now()
            self.date_BORRAR_contado = str(self.date_BORRAR_contado)[20:26]
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("INSERT into venta_dia_contado (NOMBRE_DIAx,CI_DIAx,PRODUCTO_DIAx,MONTO_DIAx,FECHA_DIAx,BORRAR) values (?,?,?,?,?,?)", ( self.Venta_dia_nombre.get(),
                self.ci_dia.get(),
                self.producto_diavar.get(),
                self.monto_dia.get(),
                self.date_diac,
                self.date_BORRAR_contado))
            self.conexion.commit()
            self.conexion.close() 
            mb.showinfo(message="Venta guardado correctamente", title="Exito!")
            self.view_a_credito()
            self.view_a_contado()
            self.view_total_cobrar()
            self.clear_text()
            self.treview_ventas_del_mes_contado()
        else:
            mb.showinfo(message="Operacion cancelado",title="Cancelado")


    def treview_ventas_del_mes_credito(self):
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM venta_dia_credito")
        self.venta_total_fetchall = self.cursor.fetchall()
        self.list_venta_total_credito = []
        for self.venta_x in self.venta_total_fetchall:
            self.list_venta_total_credito.append(self.venta_x) 
        self.conexion.close()
        self.columns_venta_credito = ('NOMBRE_CLIENTES', 'CEDULA', 'PRODUCTO_ADQUIRIDO','MONTO_PRODUCTO','FECHA_DE_COMPRA','TOTAL_COBRAR','CODIGOX')
        self.tree_venta_credito = ttk.Treeview(self.pagina5, height=15,columns=self.columns_venta_credito, show='headings')

        # define headings
        self.tree_venta_credito.heading('NOMBRE_CLIENTES', text='NOMBRE DEL CIENTE: ')
        self.tree_venta_credito.heading('CEDULA', text='CEDULA:')
        self.tree_venta_credito.heading('PRODUCTO_ADQUIRIDO', text='PRODUCTO ADQUIRIDO:')
        self.tree_venta_credito.heading('MONTO_PRODUCTO', text='MONTO DE COMPRA: ')
        self.tree_venta_credito.heading('FECHA_DE_COMPRA', text='FECHA DE COMPRA: ')
        self.tree_venta_credito.heading('TOTAL_COBRAR', text='TOTAL DE COMISION: ')
        self.tree_venta_credito.heading('CODIGOX', text='CODIGO: ')
        self.tree_venta_credito.column('#1', width=100, anchor='c')
        
        self.lista_credito_final = []
        for self.venta_creditox in self.list_venta_total_credito:
            self.credito_restar = (self.venta_creditox[3] * 10) / 100
            self.credito_10_calculado = int(self.venta_creditox[3] - int(self.credito_restar))
            self.credito_cobrear7 = (self.credito_10_calculado * 7) / 100
            self.credito_cobrear7 = int(self.credito_cobrear7)
            self.credito_cobrear7 = ("{:,}".format(self.credito_cobrear7))
            self.lista_credito_final.append((f'{self.venta_creditox[0]}',
                f'{self.venta_creditox[1]}',
                f'{self.venta_creditox[2]}',
                f'{self.venta_creditox[3]}',
                f'{self.venta_creditox[4]}',
                f'{self.credito_cobrear7}',
                f'{self.venta_creditox[5]}'))
        for self.credito_list in self.lista_credito_final:
            self.tree_venta_credito.insert('', tk.END, values=self.credito_list)
        self.tree_venta_credito.bind('<<TreeviewSelect>>',self.delete_ventas_credito)
        self.tree_venta_credito.grid(row=8, column=0, sticky='nsew')
        self.scrollbarcredito = ttk.Scrollbar(self.pagina5, orient=tk.VERTICAL, command=None)
        self.tree_venta_credito.configure(yscroll=self.scrollbarcredito.set)
        self.scrollbarcredito.grid(row=8, column=1, sticky='ns')



    def view_a_credito(self):
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT MONTO_DIA FROM venta_dia_credito")
        self.total_aCredito = self.cursor.fetchall()
        self.conexion.close()
        self.lista_venta_credito = list(self.total_aCredito)
        self.lista_monto_credito = []
        for self.monto_credito in self.lista_venta_credito:
            self.lista_monto_credito.append(self.monto_credito)
        self.total_credito_sumado = sum(tuple(map(sum, tuple(self.lista_monto_credito))))
        self.restar_monto = (self.total_credito_sumado * 10) / 100
        self.monto_calculado_10 = int(self.total_credito_sumado) - int(self.restar_monto)
        self.var_total_credito.set(self.monto_calculado_10)
        self.monto_calculado_7 = (self.monto_calculado_10 * 7) / 100
        self.monto_calculado_7 = int(self.monto_calculado_7)
        self.creditox = int(self.monto_calculado_7)
        self.monto_calculado_7 = ("{:,}".format(self.monto_calculado_7))
        self.var_credito_cobrar.set(self.monto_calculado_7)


    def treview_ventas_del_mes_contado(self):
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM venta_dia_contado")
        self.venta_total_fetchall_c = self.cursor.fetchall()
        self.list_venta_total_contado = []
        for self.venta_xc in self.venta_total_fetchall_c:
            self.list_venta_total_contado.append(self.venta_xc) 
        self.conexion.close()
        self.columns_venta_contado = ('NOMBRE_CLIENTES', 'CEDULA', 'PRODUCTO_ADQUIRIDO','MONTO_PRODUCTO','FECHA_DE_COMPRA','TOTAL_COBRAR','CODIGO')
        self.tree_venta_contado = ttk.Treeview(self.pagina5, height=5,columns=self.columns_venta_contado, show='headings')

        # define headings
        self.tree_venta_contado.heading('NOMBRE_CLIENTES', text='NOMBRE DEL CIENTE: ')
        self.tree_venta_contado.heading('CEDULA', text='CEDULA:')
        self.tree_venta_contado.heading('PRODUCTO_ADQUIRIDO', text='PRODUCTO ADQUIRIDO:')
        self.tree_venta_contado.heading('MONTO_PRODUCTO', text='MONTO DE COMPRA: ')
        self.tree_venta_contado.heading('FECHA_DE_COMPRA', text='FECHA DE VENTA: ')
        self.tree_venta_contado.heading('TOTAL_COBRAR', text='TOTAL DE COMISION: ')
        self.tree_venta_contado.heading('CODIGO', text='CODIGO: ')
        self.tree_venta_contado.column('#1', width=100, anchor='c')
        
        self.lista_contado_final = []
        for self.venta_contadox in self.list_venta_total_contado:
            self.contado_restar = (self.venta_contadox[3] * 10) / 100
            self.contado_10_calculado = int(self.venta_contadox[3] - int(self.contado_restar))
            self.contado_cobrar2 = (self.contado_10_calculado * 2) / 100
            self.contado_cobrar2 = int(self.contado_cobrar2)
            self.contado_cobrar2 = ("{:,}".format(self.contado_cobrar2))
            self.lista_contado_final.append((f'{self.venta_contadox[0]}',
                f'{self.venta_contadox[1]}',
                f'{self.venta_contadox[2]}',
                f'{self.venta_contadox[3]}',
                f'{self.venta_contadox[4]}',
                f'{self.contado_cobrar2}',
                f'{self.venta_contadox[5]}'))
        for self.contado_list in self.lista_contado_final:
            self.tree_venta_contado.insert('', tk.END, values=self.contado_list)
        self.tree_venta_contado.bind('<<TreeviewSelect>>',self.delete_ventas_contado)
        self.tree_venta_contado.grid(row=9, column=0, sticky='nsew')
        self.scrollbarCONTADO = ttk.Scrollbar(self.pagina5, orient=tk.VERTICAL, command=None)
        self.tree_venta_contado.configure(yscroll=self.scrollbarCONTADO.set)
        self.scrollbarCONTADO.grid(row=9, column=1, sticky='ns')

    def delete_ventas_contado(self,event):
        if mb.askyesnocancel(message="¿Estas seguro que deseas borrar esta venta?", title="Opciones!") == True:
            self.delete_contado = self.tree_venta_contado.item(self.tree_venta_contado.selection())['values']
            self.delete_contado_f = self.delete_contado[6]
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("DELETE FROM venta_dia_contado WHERE BORRAR={}".format(self.delete_contado_f))
            self.conexion.commit()
            self.conexion.close()
            self.treview_ventas_del_mes_contado()
            self.treview_ventas_del_mes_credito()
            self.view_a_contado()
            self.view_a_credito()
            self.treview_ventas_del_mes_credito()
            self.view_total_cobrar()
            mb.showinfo(message="Datos borrados correctamnte", title="Exito!")
        else:
            mb.showinfo(message="Operacion cancelado", title="Exito!")



    def view_a_contado(self):
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT MONTO_DIAx FROM venta_dia_contado")
        self.total_aContado = self.cursor.fetchall()
        self.conexion.close()
        self.lista_venta_contado = list(self.total_aContado)
        self.lista_monto_contado = []
        for self.monto_contado in self.lista_venta_contado:
            self.lista_monto_contado.append(self.monto_contado)
        self.total_contado_sumado = sum(tuple(map(sum, tuple(self.lista_monto_contado))))
        self.restar_monto_contado = (self.total_contado_sumado * 10) / 100
        self.monto_calculado_10_contado = int(self.total_contado_sumado) - int(self.restar_monto_contado)
        self.var_total_contado.set(self.monto_calculado_10_contado)
        self.monto_calculado_2 = (self.monto_calculado_10_contado * 2) / 100
        self.monto_calculado_2 = int(self.monto_calculado_2)
        self.contadox = int(self.monto_calculado_2)
        self.monto_final_contado = ("{:,}".format(self.monto_calculado_2))
        self.total_a_cobrar_contado.set(self.monto_final_contado)



    def delete_ventas_credito(self,event):
        if mb.askyesnocancel(message="¿Estas seguro que deseas borrar esta venta?", title="Opciones!") == True:
            self.fecha_delete = self.tree_venta_credito.item(self.tree_venta_credito.selection())['values']
            self.fecha_delete_credito = self.fecha_delete[6]
            print(self.fecha_delete_credito)
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("DELETE FROM venta_dia_credito WHERE BORRAR={}".format(self.fecha_delete_credito))
            self.conexion.commit()
            self.conexion.close()
            self.treview_ventas_del_mes_contado()
            self.treview_ventas_del_mes_credito()
            self.view_a_contado()
            self.view_a_credito()
            self.treview_ventas_del_mes_credito()
            self.view_total_cobrar()
            mb.showinfo(message="Datos borrados correctamnte", title="Exito!")
        else:
            mb.showinfo(message="Operacion cancelado", title="Exito!")



    def delete_ventas(self):
        if mb.askyesnocancel(message="¿Estas seguro, se borraran todas las ventas ingresadas hasta ahora?", title="Opciones!") == True:
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("DELETE FROM venta_dia_credito")
            self.conexion.commit()
            self.conexion.close()
            self.conexion = sqlite3.connect('xline.db')
            self.conexion.execute("DELETE FROM venta_dia_contado")
            self.conexion.commit()
            self.conexion.close()
            mb.showinfo(message="Datos borrados correctamente", title="Exito!")
            self.treview_ventas_del_mes_contado()
            self.treview_ventas_del_mes_credito()
            self.view_a_contado()
            self.view_a_credito()
            self.treview_ventas_del_mes_credito()
            self.view_total_cobrar()
        else:
            mb.showinfo(message="Datos borrados correctamente", title="Exito!")

    def view_total_cobrar(self):
        self.view_a_credito()
        self.view_a_contado()
        self.ips_resta = ((self.contadox + self.creditox) * 9) / 100
        self.neto = (int(self.contadox + self.creditox)) - int(self.ips_resta)
        self.neto = ("{:,}".format(self.neto))
        self.var_total_ips.set(self.neto)

    def consultar_cuenta_total(self):
        self.label_deuda_total=ttk.Label(self.labelframe2, text="DEUDA DE LA CARTERA:")        
        self.label_deuda_total.grid(column=4, row=0, padx=4, pady=4)
        self.total_deuda_sumado_var = tk.IntVar()
        self.entry_deuda_total=ttk.Entry(self.labelframe2, textvariable=self.total_deuda_sumado_var)
        self.entry_deuda_total.grid(column=5, row=0, padx=4, pady=4)
        self.conexion = sqlite3.connect("xline.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT presupuesto_total FROM cuenta")
        self.deuda_total_del_todos_los_clientes = self.cursor.fetchall()
        self.conexion.close()
        self.deuda_total_del_todos_los_clientes = list(self.deuda_total_del_todos_los_clientes)
        self.total_deuda_list = []
        for self.deuda in self.deuda_total_del_todos_los_clientes:
            self.total_deuda_list.append(self.deuda)
        self.total_deuda_sumado = sum(list(map(sum, list(self.total_deuda_list))))
        self.total_deuda_sumado = ("{:,}".format(self.total_deuda_sumado))
        self.total_deuda_sumado_var.set(self.total_deuda_sumado)
        
if __name__ == "__main__":
    P = Cliente()