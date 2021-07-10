$.getJSON("./resources/estados.json", function(json) {
  $(document).ready(function(){
    var estadosS = $('#estadoR');

    json.forEach((estado, index) => {
      estadosS.append(`<option value="${estado.nombre}" key="${index}">${estado.nombre}</option>`);
    });
  });
});

$.getJSON("./resources/estados-municipios.json", function(json) {
  $('#estadoR').on('change', function(e) {
    var estado = e.target.options.selectedIndex - 1;
    var municipiosS = $('#municipioR');
    municipiosS.empty();

    if (estado!=-1){
      Object.values(json)[estado].forEach(municipio => {
        municipiosS.append(`<option value="${municipio}">${municipio}</option>`)
      });
    }
  });
});


function handleRegister() {
  var indicativo = document.getElementById("indicativoR").value;
  var contrasena = document.getElementById("contrasenaR").value;
  var nombre = document.getElementById("nombreR").value;
  var apellidoP = document.getElementById("apellidoPR").value;
  var apellidoM = document.getElementById("apellidoMR").value;
  var estado = document.getElementById("estadoR").value;
  var municipio = document.getElementById("municipioR").value;

  const dataRegister ={ indicativo, contrasena ,nombre, apellidoP, apellidoM, estado, municipio };
  
  if(indicativo == "" || contrasena == "" || nombre == "" || apellidoP == "" || apellidoM == "" || estado == "" || municipio == ""){
    var formRegister = document.querySelectorAll('#register');
    formRegister[0].classList.remove('was-validated');
    formRegister[0].classList.add('was-validated');
  }
  else{
    console.log("Registrar:",dataRegister)
  }
}

function handleLogin(){
  var indicativo = document.getElementById("indicativoL").value;
  var contrasena = document.getElementById("contrasenaL").value;

  const dataRegister ={ indicativo, contrasena };
  
  if(indicativo == "" || contrasena == ""){
    var formLogin = document.querySelectorAll('#login');
    formLogin[0].classList.remove('was-validated');
    formLogin[0].classList.add('was-validated');
  }
  else{
    console.log("Login:",dataRegister);
  }
}