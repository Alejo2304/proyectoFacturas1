from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Empresa import Empresa
from control.ControlEmpresa import ControlEmpresa




vistaEmpresas=Blueprint("vistaEmpresas",__name__,static_folder="static",template_folder="templates")

@vistaEmpresas.route("/vistaEmpresas", methods=['GET', 'POST'], defaults={'path': ''})
@vistaEmpresas.route("/vistaEmpresas/<path:path>", methods=['GET', 'POST'])
def vista_Empresas(path):
    """
    This function handles the logic for the 'vista_Empresas' view.

    It retrieves a list of clients, performs pagination, and handles various form submissions.

    Returns:
        A rendered template with the necessary data for the view.
    """
    
    arregloEmpresas=[]
    empresa = {
    'codigo': '',
    'nombre': '',
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
    objControlEmpresa=ControlEmpresa(None)
    arregloEmpresas=objControlEmpresa.listar()

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
    
    paginacion=updatePagination(arregloEmpresas)

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        cod=markupsafe.escape(request.form['txtCodigo'])
        nom=markupsafe.escape(request.form['txtNombre'])
        
        paginacion['itemsxpagina']=markupsafe.escape(request.form.get('combo2'))
        

        btnMsg=markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')

        
        empresa = {
        'codigo': cod,
        'nombre': nom
        }

        if request.form.get('combo2') != paginacion['itemsxpagina']:
            updatePagination(arregloEmpresas)

            return render_template('/vistaEmpresas.html',ema=ema,arregloEmpresas=arregloEmpresas,empresa=empresa,paginacion=paginacion)
        
        if bt=='Guardar':
            try:
                objEmpresa= Empresa(cod,nom)
                objControlEmpresa = objControlEmpresa(objEmpresa)
                objControlEmpresa.guardar()  

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaEmpresas')	
        	
        elif bt=='Consultar':
            #pass
            try:    
                objEmpresa= Empresa(cod,nom)
                objControlEmpresa = objControlEmpresa(objEmpresa)
                objControlEmpresa.consultar()

                empresa['codigo']=objControlEmpresa.objEmpresa.getCodigo()
                empresa['nombre']=objControlEmpresa.objEmpresa.getNombre()

                return render_template('/vistaEmpresas.html',ema=ema,arregloEmpresas=arregloEmpresas,empresa=empresa,paginacion=paginacion)


            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)

            
            return redirect('/vistaEmpresas')  
        
        elif bt=='Modificar':
            try:
                objEmpresa= Empresa(cod,nom)
                objControlEmpresa = objControlEmpresa(objEmpresa)
                objControlEmpresa.modificar() 

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaEmpresas')	
        	
        elif bt=='Borrar':
            try:
                objEmpresa= Empresa(cod,nom)
                objControlEmpresa = objControlEmpresa(objEmpresa)
                objControlEmpresa.borrar()       
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaEmpresas')
        
        
        elif bt=='BorrarVarios':
            pass
    return render_template('/vistaEmpresas.html',ema=ema,arregloEmpresas=arregloEmpresas,empresa=empresa,paginacion=paginacion)

