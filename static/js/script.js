function updateOptions() {
  var gusto1 = document.getElementById('gusto1');
  var gusto2 = document.getElementById('gusto2');
  var disguto = document.getElementById('disgusto');
  
  // Habilita todas las opciones en gusto2
  for (var i = 0; i < gusto2.options.length; i++) {
    gusto2.options[i].disabled = false;
  }
  
  // Busca la opción seleccionada en gusto1 y deshabilítala en gusto2
  var selectedOption = gusto1.options[gusto1.selectedIndex].value;
  for (var i = 0; i < gusto2.options.length; i++) {
    if (gusto2.options[i].value === selectedOption) {
      gusto2.options[i].disabled = true;
    }
  }

  // Busca la opcion seleccionada en gusto2 y deshabilitala en gusto1
  var selectedOption = gusto2.options[gusto2.selectedIndex].value;
  for (var i = 0; i < gusto1.options.length; i++) {
    if (gusto1.options[i].value === selectedOption) {
      gusto1.options[i].disabled = true;
    }
  }

  // Busca la opcion seleccionada en gusto2 y deshabilitala en gusto1
  var selectedOption = gusto1.options[gusto1.selectedIndex].value;
  var selectedOption2 = gusto2.options[gusto2.selectedIndex].value;
  
  for (var i = 0; i < disguto.options.length; i++) {
    if (disguto.options[i].value === selectedOption){
      disguto.options[i].disabled = true;
    }
    else if(disguto.options[i].value === selectedOption2){
      disguto.options[i].disabled = true;
    }
  }
}

function visibleInput(){

  let query = document.getElementById('query').value
  let input = document.getElementById('seleccion_nodo_raiz')
  
  if (query === '2' || query ==='6' || query ==='7' ){
    input.style.display='inline';
  }else{
    input.style.display='none';
  }
  }