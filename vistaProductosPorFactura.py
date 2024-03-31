from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.ProductosPorFactura import ProductosPorFactura
from control.ControlProductosPorFactura import ControlProductosPorFactura




vistaProductosPorFactura=Blueprint("vistaProductosPorFactura",__name__,static_folder="static",template_folder="templates")

@vistaProductosPorFactura.route("/vistaProductosPorFactura",methods = ['GET', 'POST'])

@vistaProductosPorFactura.route('/submit', methods=['POST'])

@vistaProductosPorFactura.route("/")

def vista_ProductosPorFactura():
    """
    This function handles the logic for the 'vista_Facturas' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloFacturas=[]
    productosporfactura = {
    'factura': '',
    'producto': '',
    'cantidad':'',
    'subtotal':''
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
    objControl=ControlProductosPorFactura(None)
    arregloFacturas=objControl.listar()

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
        fac=markupsafe.escape(request.form['txtFactura'])
        pro=markupsafe.escape(request.form['txtProducto'])
        can=markupsafe.escape(request.form['txtCantidad'])
        sub=markupsafe.escape(request.form['txtSubtotal'])
        paginacion['itemsxpagina'] = markupsafe.escape(request.form.get('combo2'))

        btnMsg = markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')


        productosporfactura = {
        'factura': fac,
        'producto': pro,
        'cantidad':can,
        'subtotal':sub
        }

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloFacturas)

            return render_template('/vistaProductosPorFactura.html',ema=ema,arregloFacturas=arregloFacturas,productosporfactura=productosporfactura,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objFactura=ProductosPorFactura(fac,pro,can,sub)
                objControlFactura=ControlProductosPorFactura(objFactura)
                objControlFactura.guardar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductosPorFactura')	
        
        elif bt=='Consultar':
            try:
                objFactura=ProductosPorFactura(fac,pro,can,sub)
                objControlFactura=ControlProductosPorFactura(objFactura)
                objControlFactura.consultar()

                productosporfactura['factura'] = objControlFactura.objProductosPorFactura.getFactura()
                productosporfactura['producto'] = objControlFactura.objProductosPorFactura.getProducto()
                productosporfactura['cantidad'] = objControlFactura.objProductosPorFactura.getCantidad()
                productosporfactura['subtotal'] = objControlFactura.objProductosPorFactura.getSubtotal()

                return render_template('/vistaProductosPorFactura.html',ema=ema,arregloFacturas=arregloFacturas,productosporfactura=productosporfactura,paginacion=paginacion)
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductosPorFactura')
        
        elif bt== 'Modificar':
            try:
                objFactura=ProductosPorFactura(fac,pro,can,sub)
                objControlFactura=ControlProductosPorFactura(objFactura)
                objControlFactura.modificar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductosPorFactura')
        
        elif bt== 'Borrar':
            pass
            try:
                objFactura=ProductosPorFactura(fac,pro,can,sub)
                objControlFactura=ControlProductosPorFactura(objFactura)
                objControlFactura.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductosPorFactura')
        
        elif bt== 'BorrarVarios':
            pass
    return render_template('/vistaProductosPorFactura.html',ema=ema,arregloFacturas=arregloFacturas,productosporfactura=productosporfactura,paginacion=paginacion)