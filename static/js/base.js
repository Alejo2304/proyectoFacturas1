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

//This function update the value of txtValorUnitario on vistaFactura.html
$(document).ready(function(){
    $(document).on('change', '#txtProductos', function(){
        var selectedValue = $('option:selected', this).data('valorunitario');
        $(this).closest('tr').find("#txtValorUnitario").val(selectedValue);
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
	//document.getElementById("txtNumero").value = 0;
}

function disableTotal() {
	document.getElementById("txtTotal").disabled = true;
	//document.getElementById("txtTotal").value = "NULL";
}

function disableFecha() {
	document.getElementById("txtFecha").disabled = true;
	//document.getElementById("txtFecha").value = "";
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

function getOptionValues() {
    // Get the select element as a whole
    let selectElement = document.getElementById('txtProductos');
    if (selectElement === null) {
        console.error('selectElement is null');
        return [];
    }
    // Get the selected option
    let selectedOption = selectElement.value;
    
    // Get the options as an array of objects
	let optionValues = Array.from(selectElement.options)
		.filter(option => !option.disabled)
		.map(option => ({
			value: option.value,
			valorunitario: option.dataset.valorunitario
		}));
    // Remove the selected option from the Array
    optionValues = optionValues.filter(option => option.value !== selectedOption);
    console.log(optionValues);
    return optionValues;
}

/**
 * Adds a new row to the specified table.
 * 
 * @param {string} tableID - The ID of the table to add the row to.
 */
function addRow(tableID) {
	
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	var row = table.insertRow(rowCount);
	var colCount = table.rows[0].cells.length;
	var optionValues = getOptionValues();

	selectElement = document.getElementById('txtProductos');
	selectElement.id = "txtProductos" + (rowCount-1);
	selectElement.name = "txtProductos" + (rowCount-1);

	selectElement = document.getElementById('txtValorUnitario');
	selectElement.id = "txtValorUnitario" + (rowCount-1);
	selectElement.name = "txtValorUnitario" + (rowCount-1);

	selectElement = document.getElementById('txtCantidad');
	selectElement.id = "txtCantidad" + (rowCount-1);
	selectElement.name = "txtCantidad" + (rowCount-1);

	selectElement = document.getElementById('txtSubtotal');
	selectElement.id = "txtSubtotal" + (rowCount-1);
	selectElement.name = "txtSubtotal" + (rowCount-1);

	// Create a new select element
	var select = document.createElement("select");
	select.id = "txtProductos";
	select.name = "txtProductos";

	// Add options to the select element
	optionValues.forEach(function(optionValue) {
		var option = document.createElement("option");
		option.value = optionValue.value;
		option.text = optionValue.value;
		option.dataset.valorunitario = optionValue.valorunitario; 
		select.appendChild(option);
	});

	defaultOption = document.createElement("option");
	defaultOption.text = "Seleccione el producto.";
	defaultOption.selected = true;
	defaultOption.disabled = true;
	select.appendChild(defaultOption);
	

	// Add the select element to the new row
	var newCell = row.insertCell(0);
	newCell.appendChild(select);

	// Add the remaining cells to the new row
	for(var i = 1; i < colCount; i++) {
		var newCell = row.insertCell(i);
		newCell.innerHTML = table.rows[1].cells[i].innerHTML;
		var childElements = newCell.children;
		for(var j = 0; j < childElements.length; j++) {
			if (childElements[j].id) {
				var oldId = childElements[j].id;
				var newId = oldId.replace(/\d+$/, '');
				childElements[j].id = newId;
			}
		}
	}
}
