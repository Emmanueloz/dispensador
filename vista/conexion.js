
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

// Función para consultar registros desde la base de datos
function consultarRegistros() {
  firebase.database().ref('test/estados').once('value')
    .then((snapshot) => {
      const estados = snapshot.val();
      if (estados) {
        const registros = Object.keys(estados).filter((key) => {
          // Verificar si el nombre del registro comienza con "contenedor", "dispensador" o "recipiente"
          return key.startsWith('contenedor') || 
                 key.startsWith('dispensador') || 
                 key.startsWith('recipiente');
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


// Función para mostrar registros en la vista HTML
function mostrarListaRegistros(registros) {
    // Obtener el contenedor donde se mostrarán los registros
    const registrosContainer = document.getElementById('registrosContainer');
    
    // Limpiar el contenedor antes de agregar los nuevos registros
    registrosContainer.innerHTML = '';

    // Crear un elemento para cada registro y agregarlo al contenedor
    registros.forEach(registro => {
        const registroElement = document.createElement('div');
        registroElement.textContent = registro;
        registrosContainer.appendChild(registroElement);
    });
}


function mostrarMensaje(message) {
  alert(message);
}

initializeFirebase();

consultarRegistros();