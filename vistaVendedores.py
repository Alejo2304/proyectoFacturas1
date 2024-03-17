from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Persona import Persona
from modelo.Vendedor import Vendedor
from control.ControlVendedor import ControlVendedor




vistaVendedores=Blueprint("vistaVendedores",__name__,static_folder="static",template_folder="templates")

@vistaVendedores.route("/vistaVendedores",methods = ['GET', 'POST'])

@vistaVendedores.route('/submit', methods=['POST'])

@vistaVendedores.route("/")

def vista_Vendedores():
    """
    This function handles the logic for the 'vista_Vendedores' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloVendedores=[]
    vendedor = {
    'codigo': '',
    'nombre': '',
    'telefono':'',
    'email':'',
    'carnet':'',
    'direccion':''
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
    objControlVendedor=ControlVendedor(None)
    arregloVendedores=objControlVendedor.listar()

    def updatePagination(arreglo):
        totalItems=len(arreglo)
        itemsxpagina=request.form.get('combo2')
        if itemsxpagina==None:
            itemsxpagina=5

        paginaActiva = request.args.get('paginaActiva')
        if paginaActiva==None: 
            paginaActiva=1  

        itemsxpagina, paginaActiva = int(itemsxpagina), int(paginaActiva)
        numPaginas=math.ceil(totalItems/int(itemsxpagina))
        posInicial=(paginaActiva-1)*itemsxpagina
        posFinal=posInicial+itemsxpagina

        if posFinal>totalItems:
            posFinal=totalItems

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
    
    paginacion=updatePagination(arregloVendedores)

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        #print("Debug: ", request.form)  # Print all form data
        #print("Debug dir: ", request.form.get('txtDireccion'))  # Print the value of 'txtDireccion'
        bt=markupsafe.escape(request.form.get('bt'))
        cod=markupsafe.escape(request.form['txtCodigo'])
        nom=markupsafe.escape(request.form['txtNombre'])
        tel=markupsafe.escape(request.form['txtTelefono'])
        ema=markupsafe.escape(request.form['txtEmail'])
        car=markupsafe.escape(request.form['txtCarnet'])
        dir=markupsafe.escape(request.form['txtDireccion'])
        paginacion['itemsxpagina']=markupsafe.escape(request.form.get('combo2'))
        #print("Debug dir: ", request.form.get('txtDireccion'), "SECOND TEST: ", dir)  # Print the value of 'txtDireccion'

        btnMsg=markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')

        
        vendedor = {
        'codigo': cod,
        'nombre': nom,
        'telefono':tel,
        'email': ema,
        'carnet': car,
        'direccion': dir
        }

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloVendedores)

            return render_template('/vistaVendedores.html',ema=ema,arregloVendedores=arregloVendedores,vendedor=vendedor,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objVendedor= Vendedor(car, dir)
                objControlVendedor= ControlVendedor(objPersona,objVendedor)
                objControlVendedor.guardar()  

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaVendedores')	
        	
        elif bt=='Consultar':
            #pass
            try:    
                objPersona= Persona(cod,nom,tel,ema)
                objVendedor= Vendedor(car, dir)
                objControlVendedor= ControlVendedor(objPersona,objVendedor)
                objControlVendedor.consultar()

                vendedor['codigo']=objControlVendedor.objVendedor.getCodigo()
                vendedor['nombre']=objControlVendedor.objVendedor.getNombre()
                vendedor['telefono']=objControlVendedor.objVendedor.getTelefono()
                vendedor['email']=objControlVendedor.objVendedor.getEmail()
                vendedor['carnet']=objControlVendedor.objVendedor.getCarnet()
                vendedor['direccion']=objControlVendedor.objVendedor.getDireccion()

                return render_template('/vistaVendedores.html',ema=ema,arregloVendedores=arregloVendedores,vendedor=vendedor,paginacion=paginacion)


            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)

            
            return redirect('/vistaVendedores')  
        elif bt=='Modificar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objVendedor= Vendedor(car,dir)
                objControlVendedor= ControlVendedor(objPersona,objVendedor)
                objControlVendedor.modificar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaVendedores')	
        	
        elif bt=='Borrar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objVendedor= Vendedor(car,dir)
                objControlVendedor= ControlVendedor(objPersona,objVendedor)
                objControlVendedor.borrar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaVendedores')
        
        
        elif bt=='BorrarVarios':
            pass
    return render_template('/vistaVendedores.html',ema=ema,arregloVendedores=arregloVendedores,vendedor=vendedor,paginacion=paginacion)

