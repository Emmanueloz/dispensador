
// https://firebase.google.com/docs/web/setup#available-libraries

const firebaseConfig = {
  apiKey: "AIzaSyD3l2W0fhM7QfF3PhvSK3dU5Sghsn7ORBs",
  authDomain: "aplicacionesiot-1622a.firebaseapp.com",
  databaseURL: "https://aplicacionesiot-1622a-default-rtdb.firebaseio.com",
  projectId: "aplicacionesiot-1622a",
  storageBucket: "aplicacionesiot-1622a.appspot.com",
  messagingSenderId: "801264676158",
  appId: "1:801264676158:web:b39b19991c7167cc89106f"
};
function initializeFirebase() {
  try {
    firebase.initializeApp(firebaseConfig);
    console.log("¡Conexión exitosa a Firebase!");
  } catch (error) {
    console.error("Error al conectar a Firebase:", error);
    alert("¡Error al conectar a Firebase!");
  }
}

function consultarRegistros() {
  firebase.database().ref('test/estados').once('value')
    .then((snapshot) => {
      const estados = snapshot.val();
      if (estados) {
        const registros = Object.keys(estados).filter((key) => {
          return key.startsWith('contenedor') || 
                 key.startsWith('dispensador') || 
                 key.startsWith('recipiente') ||
                 key.startsWith('tResultado');
        }).map((key) => {
          const estado = estados[key];
          return `${key} - Estado: ${estado.estado}`;
        });
        mostrarListaRegistros(registros);
      } else {
        mostrarMensaje("No hay registros de estados en la base de datos.");
      }
    })
    .catch((error) => {
      console.error("Error al obtener datos de Firebase:", error);
      mostrarMensaje("¡Error al obtener datos de Firebase!");
    });
}


function mostrarListaRegistros(registros) {
  registros.forEach((registro) => {
    const [tipo, estado] = registro.split(' - Estado: ');
    switch (tipo) {
      case 'contenedor1':
        document.getElementById('ContenedorAgua').textContent = `Contenedor de agua: ${estado}`;
        break;
      case 'contenedor2':
        document.getElementById('ContenedorComida').textContent = `Contenedor de comida: ${estado}`;
        break;
      case 'dispensador1':
        document.getElementById('DispensadorAgua').textContent = `Dispensador de agua: ${estado}`;
        break;
      case 'dispensador2':
        document.getElementById('DispensadorComida').textContent = `Dispensador de comida: ${estado}`;
        break;
      case 'recipiente1':
        document.getElementById('RecienteAgua').textContent = `Recipiente de agua: ${estado}`;
        break;
      case 'recipiente2':
        document.getElementById('RecienteComida').textContent = `Recipiente de comida: ${estado}`;
        break;
      case 'tResultado1':
        document.getElementById('Resultado1').textContent = `El dispensador de agua: ${estado}`;
        break;
      case 'tResultado2':
        document.getElementById('Resultado2').textContent = `El dispensador de comida: ${estado}`;
        break;
      default:
        break;
    }
  });
}


initializeFirebase();

consultarRegistros();