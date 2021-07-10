function handleRegister() {
  var indicativo = document.getElementById("indicativoR").value;
  var contrasena = document.getElementById("contrasenaR").value;
  var nombre = document.getElementById("nombreR").value;
  var apellidoP = document.getElementById("apellidoPR").value;
  var apellidoM = document.getElementById("apellidoMR").value;
  var estado = document.getElementById("estadoR").value;
  var municipio = document.getElementById("municipioR").value;

  const dataRegister ={ indicativo, contrasena ,nombre, apellidoP, apellidoM, estado, municipio };
  console.log("Registrar:",dataRegister)
}

function handleLogin(){
  var indicativo = document.getElementById("indicativoL").value;
  var contrasena = document.getElementById("contrasenaL").value;

  const dataRegister ={ indicativo, contrasena };
  console.log("Login:",dataRegister)
}