from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Factura import Factura
from control.ControlFactura import ControlFactura




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
        num=markupsafe.escape(request.form['txtNumero'])
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

            return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,factura=factura,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objFactura=Factura(num,fec,tot,cli,ven)
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

                return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,factura=factura,paginacion=paginacion)
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaFacturas')
        
        elif bt== 'Modificar':
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
        
        elif bt== 'BorrarVarios':
            pass
    return render_template('/vistaFacturas.html',ema=ema,arregloFacturas=arregloFacturas,factura=factura,paginacion=paginacion)