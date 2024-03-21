from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Producto import Producto
from control.ControlProducto import ControlProducto




vistaProductos=Blueprint("vistaProductos",__name__,static_folder="static",template_folder="templates")

@vistaProductos.route("/vistaProductos",methods = ['GET', 'POST'])

@vistaProductos.route('/submit', methods=['POST'])

@vistaProductos.route("/")

def vista_Productos():
    """
    This function handles the logic for the 'vista_Productos' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloProductos=[]
    producto = {
    'codigo': '',
    'nombre': '',
    'stock':'',
    'valorUnitario':'',
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
    
    paginacion=updatePagination(arregloProductos)

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        cod=markupsafe.escape(request.form['txtCodigo'])
        nom=markupsafe.escape(request.form['txtNombre'])
        sto=markupsafe.escape(request.form['txtStock'])
        val=markupsafe.escape(request.form['txtValorUnitario'])
        paginacion['itemsxpagina'] = markupsafe.escape(request.form.get('combo2'))

        btnMsg = markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')


        producto = {
        'codigo': cod,
        'nombre': nom,
        'stock': sto,
        'valorUnitario': val
        }

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloProductos)

            return render_template('/vistaProductos.html',ema=ema,arregloProductos=arregloProductos,producto=producto,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objProducto=Producto(cod,nom,sto,val)
                objControlProducto=ControlProducto(objProducto)
                objControlProducto.guardar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductos')	
        
        elif bt=='Consultar':
            try:
                objProducto=Producto(cod,nom,sto,val)
                objControlProducto=ControlProducto(objProducto)
                objControlProducto.consultar()

                producto['codigo'] = objControlProducto.objProducto.getCodigo()
                producto['nombre'] = objControlProducto.objProducto.getNombre()
                producto['stock'] = objControlProducto.objProducto.getStock()
                producto['valorUnitario'] = objControlProducto.objProducto.getValorUnitario()

                return render_template('/vistaProductos.html',ema=ema,arregloProductos=arregloProductos,producto=producto,paginacion=paginacion)
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductos')
        
        elif bt== 'Modificar':
            try:
                objProducto=Producto(cod,nom,sto,val)
                objControlProducto=ControlProducto(objProducto)
                objControlProducto.modificar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductos')
        
        elif bt== 'Borrar':
            try:
                objProducto=Producto(cod,nom,sto,val)
                objControlProducto=ControlProducto(objProducto)
                objControlProducto.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaProductos')
        
        elif bt== 'BorrarVarios':
            pass
    return render_template('/vistaProductos.html',ema=ema,arregloProductos=arregloProductos,producto=producto,paginacion=paginacion)