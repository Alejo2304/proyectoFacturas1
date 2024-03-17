from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Persona import Persona
from modelo.Cliente import Cliente
from control.ControlCliente import ControlCliente




vistaClientes=Blueprint("vistaClientes",__name__,static_folder="static",template_folder="templates")

@vistaClientes.route("/vistaClientes",methods = ['GET', 'POST'])

@vistaClientes.route('/submit', methods=['POST'])

@vistaClientes.route("/")

def vista_Clientes():
    """
    This function handles the logic for the 'vista_Clientes' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloClientes=[]
    cliente = {
    'codigo': '',
    'nombre': '',
    'telefono':'',
    'email':'',
    'credito':0
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
    objControlCliente=ControlCliente(None)
    arregloClientes=objControlCliente.listar()

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
    
    paginacion=updatePagination(arregloClientes)

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        cod=markupsafe.escape(request.form['txtCodigo'])
        nom=markupsafe.escape(request.form['txtNombre'])
        tel=markupsafe.escape(request.form['txtTelefono'])
        ema=markupsafe.escape(request.form['txtEmail'])
        cre=markupsafe.escape(request.form['txtCredito'])
        paginacion['itemsxpagina']=markupsafe.escape(request.form.get('combo2'))
        

        btnMsg=markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')

        
        cliente = {
        'codigo': cod,
        'nombre': nom,
        'telefono':tel,
        'email':ema,
        'credito':cre
        }

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloClientes)

            return render_template('/vistaClientes.html',ema=ema,arregloClientes=arregloClientes,cliente=cliente,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.guardar()  

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')	
        	
        elif bt=='Consultar':
            #pass
            try:    
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.consultar()

                cliente['codigo']=objControlCliente.objCliente.getCodigo()
                cliente['nombre']=objControlCliente.objCliente.getNombre()
                cliente['telefono']=objControlCliente.objCliente.getTelefono()
                cliente['email']=objControlCliente.objCliente.getEmail()
                cliente['credito']=objControlCliente.objCliente.getCredito()

                return render_template('/vistaClientes.html',ema=ema,arregloClientes=arregloClientes,cliente=cliente,paginacion=paginacion)


            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)

            
            return redirect('/vistaClientes')  
        elif bt=='Modificar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.modificar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')	
        	
        elif bt=='Borrar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.borrar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')
        
        
        elif bt=='BorrarVarios':
            pass
    return render_template('/vistaClientes.html',ema=ema,arregloClientes=arregloClientes,cliente=cliente,paginacion=paginacion)

