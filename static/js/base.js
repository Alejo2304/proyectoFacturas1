$(document).ready(function(){
	// Activate tooltip
	$('[data-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});
	$("#btnAgregarItem").click(function(event) {
	   return false;
    });
	$("#btnBorrarItem").click(function(event) {
	   return false;
    });
	 	
});


function agregarItem(IDdesde, IDhasta){
    var option = document.createElement("option");
    option.text = document.getElementById(IDdesde).value;
    document.getElementById(IDhasta).add(option);
    removerItem(IDdesde);
	selectTodos(IDhasta);
  }

 function removerItem(IDelemento){
	var comboBox = document.getElementById(IDelemento);
    comboBox = comboBox.options[comboBox.selectedIndex];
    comboBox.remove();
	selectTodos(IDelemento);
  }

  function selectTodos(IDelemento) {
    var elementos = document.getElementById(IDelemento);
    elementos = elementos.options;
    for (var i = 0; i < elementos.length; i++) {
        elementos[i].selected = "true";
    }
}

function actualizarValorSeleccionado(combo,txtOculto) {
	var select = document.getElementById(combo);
	var valorSeleccionado = select.value;
	document.getElementById(txtOculto).value = valorSeleccionado;
  }

function enableNumero() {
	document.getElementById("txtNumero").disabled = false;
	document.getElementById("txtNumero").focus();
  }

function disableNumero() {
document.getElementById("txtNumero").disabled = true;
document.getElementById("txtNumero").value = "";
}

function disableTotal() {
	document.getElementById("txtTotal").disabled = true;
	document.getElementById("txtTotal").value = "";
}

function disableFecha() {
	document.getElementById("txtFecha").disabled = true;
	document.getElementById("txtFecha").value = "";
}

function disableCliente() {
	document.getElementById("txtCliente").disabled = true;
	document.getElementById("txtCliente").value = "";
}

function disableVendedor() {
	document.getElementById("txtVendedor").disabled = true;
	document.getElementById("txtVendedor").value = "";
}


function actualizarSubtotal(){
	var valorUnitario = document.getElementById("txtValorUnitario").value;
	var cantidad = document.getElementById("txtCantidad").value;
	var subtotal = cantidad * valorUnitario;
	document.getElementById("txtSubtotal").value = subtotal;
}