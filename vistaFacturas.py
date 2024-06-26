from flask import Blueprint,render_template,session,redirect,request
from datetime import datetime
import markupsafe
import math

from modelo.Factura import Factura
from control.ControlFactura import ControlFactura
from modelo.ProductosPorFactura import ProductosPorFactura
from control.ControlProductosPorFactura import ControlProductosPorFactura
from modelo.Cliente import Cliente
from control.ControlCliente import ControlCliente
from modelo.Vendedor import Vendedor
from modelo.Persona import Persona
from control.ControlVendedor import ControlVendedor
from modelo.Producto import Producto
from control.ControlProducto import ControlProducto


vistaFacturas=Blueprint("vistaFacturas",__name__,static_folder="static",template_folder="templates")
@vistaFacturas.route("/vistaFacturas",methods = ['GET', 'POST'])

@vistaFacturas.route('/submit', methods=['POST'])

@vistaFacturas.route("/")



def vista_Facturas():
    
    """
    This function handles the logic for the 'vista_Facturas' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloFacturas=[]
    arregloProductosPorFactura=[]
    arregloClientes=[]
    arregloVendedores=[]
    arregloProductos=[]

    factura = {
    'numero': '',
    'fecha': '',
    'total':'',
    'cliente':'',
    'vendedor':''
    }
    
    if 'ema' in session:
        ema=session['ema']
        permisoParaEntrar=False
        matRolesDelUsuario = session.get('matRolesDelUsuario', [])
        i=0
        while i < len(matRolesDelUsuario):
            if matRolesDelUsuario[i][1] == "admin":
                permisoParaEntrar = True
            i+=1
        if permisoParaEntrar==False:
            return render_template('menu.html',ema=ema)
    else:
        return redirect('/')  
    msg="ok"
    objControlFactura=ControlFactura(None)
    arregloFacturas=objControlFactura.listar()

    objControlCliente=ControlCliente(None)
    arregloClientes=objControlCliente.listar()

    objControlVendedor=ControlVendedor(None)
    arregloVendedores=objControlVendedor.listar()

    objControlProducto=ControlProducto(None)
    arregloProductos=objControlProducto.listar()
    

    def updatePagination(arreglo):
        totalItems=len(arreglo)
        itemsxpagina=request.form.get('combo2')
        if itemsxpagina==None:
            itemsxpagina=5
        
        paginaActiva = request.args.get('paginaActiva')
        if paginaActiva==None: 
            paginaActiva=1

        itemsxpagina, paginaActiva = int(itemsxpagina), int(paginaActiva)
        numPaginas = math.ceil(totalItems / itemsxpagina)
        posInicial = (paginaActiva - 1) * itemsxpagina
        posFinal = posInicial + itemsxpagina

        if posFinal > totalItems:
            posFinal = totalItems

        rango=range(posInicial,posFinal)
        itemsMostrados=len(rango)
        itemsCombo2=[5,10,20,30,50,100,200,1]
        paginacion={
            "itemsxpagina":itemsxpagina,
            "totalItems":totalItems,
            "numPaginas":numPaginas,
            "paginaActiva":paginaActiva,
            "posInicial":posInicial,
            "rango":rango,
            "itemsMostrados":itemsMostrados,
            "itemsCombo2":itemsCombo2
            }
        return paginacion
    
    paginacion=updatePagination(arregloFacturas)
    

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        num=markupsafe.escape(request.form.get('txtNumero'))
        fec=markupsafe.escape(request.form['txtFecha'])
        tot=markupsafe.escape(request.form['txtTotal'])
        cli=markupsafe.escape(request.form['txtCliente'])
        ven=markupsafe.escape(request.form['txtVendedor'])
        paginacion['itemsxpagina'] = markupsafe.escape(request.form.get('combo2'))


        btnMsg = markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')

        factura = {
        'numero': num,
        'fecha': fec,
        'total':tot,
        'cliente':cli,
        'vendedor':ven
        }

        

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloFacturas)

            return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,arregloClientes=arregloClientes, arregloProductos= arregloProductos,arregloProductosPorFactura=arregloProductosPorFactura,arregloVendedores=arregloVendedores,factura=factura,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objFactura=Factura(None,fec,tot,cli,ven)
                objControlFactura=ControlFactura(objFactura)
                objControlFactura.guardar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaFacturas')	
        
        elif bt=='Consultar':
            try:
                objFactura=Factura(num,fec,tot,cli,ven)
                objControlFactura=ControlFactura(objFactura)
                objControlFactura.consultar()

                factura['numero'] = objControlFactura.objFactura.getNumero()
                factura['fecha'] = objControlFactura.objFactura.getFecha()
                factura['total'] = objControlFactura.objFactura.getTotal()
                factura['cliente'] = objControlFactura.objFactura.getCliente()
                factura['vendedor'] = objControlFactura.objFactura.getVendedor()
                #This line convert the date to a string
                factura['fecha'] = factura['fecha'].strftime("%Y-%m-%d")
                
                #########################################################################
                #This block of code is used to get the products associated with the invoice
                objProductosPorFactura = ProductosPorFactura(None, None, None, None)
                objProductosPorFactura.setFactura(factura['numero'])
                objControlProductosPorFactura = ControlProductosPorFactura(objProductosPorFactura)
                arregloProductosPorFactura = objControlProductosPorFactura.consultarPorFactura()

                #########################################################################
                #This block of code is used to get the client associated with the invoice
                objPersona = Persona(None, None, None, None)
                objCliente = Cliente(None, None)
                objControlCliente = ControlCliente(objPersona, objCliente)
                objControlCliente.consultarPorCliente(factura['cliente'])
                factura['cliente'] = f"{objControlCliente.objCliente.getCodigo()} - {objControlCliente.objCliente.getNombre()}"

                ######################################################################### 
                #This block of code is used to get the seller associated with the invoice
                objPersona = Persona(None, None, None, None)
                objVendedor = Vendedor(None, None)
                objControlVendedor = ControlVendedor(objPersona, objVendedor)
                objControlVendedor.consultarPorVendedor(factura['vendedor'])
                factura['vendedor'] = f"{objControlVendedor.objVendedor.getCodigo()} - {objControlVendedor.objVendedor.getNombre()}"
            
                #########################################################################
                return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,arregloClientes=arregloClientes, arregloProductos= arregloProductos, arregloProductosPorFactura=arregloProductosPorFactura, arregloVendedores=arregloVendedores,factura=factura,paginacion=paginacion)
            except Exception as objException:
                print("diablos")
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaFacturas')
        
        elif bt=='Modificar':
            try:
                objFactura=Factura(num,fec,tot,cli,ven)
                objControlFactura=ControlFactura(objFactura)
                objControlFactura.modificar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaFacturas')
        
        elif bt== 'Borrar':
            try:
                objFactura=Factura(num,fec,tot,cli,ven)
                objControlFactura=ControlFactura(objFactura)
                objControlFactura.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaFacturas')
        
        elif bt== 'GuardarProductoPorFactura':
            '''
            for productos in arregloProductosPorFactura:
                objProductosPorFactura = ProductosPorFactura(None,productos[0],productos[1],productos[2],productos[3])
                objControlProductosPorFactura = ControlProductosPorFactura(objProductosPorFactura)
                objControlProductosPorFactura.guardar()
            '''
            #a llamar a productosPorFactura.guardar()
            pass
        elif bt== 'BorrarVarios':
            pass
    return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,arregloClientes=arregloClientes,arregloVendedores=arregloVendedores,arregloProductosPorFactura=arregloProductosPorFactura,arregloProductos= arregloProductos,factura=factura,paginacion=paginacion)