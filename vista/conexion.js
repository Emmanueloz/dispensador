// https://firebase.google.com/docs/web/setup#available-libraries

const firebaseConfig = {
  apiKey: "AIzaSyD3l2W0fhM7QfF3PhvSK3dU5Sghsn7ORBs",
  authDomain: "aplicacionesiot-1622a.firebaseapp.com",
  databaseURL: "https://aplicacionesiot-1622a-default-rtdb.firebaseio.com",
  projectId: "aplicacionesiot-1622a",
  storageBucket: "aplicacionesiot-1622a.appspot.com",
  messagingSenderId: "801264676158",
  appId: "1:801264676158:web:b39b19991c7167cc89106f",
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
initializeFirebase();

  /* mustra los estados de agua y comida, haci como tambien esta pendiente de cualquier cambio */

firebase
  .database()
  .ref("test/estados")
  .on("value", (snapshot) => {
    const estados = snapshot.val();
    if (estados) {
      const registros = Object.keys(estados)
        .filter((key) => {
          return (
            key.startsWith("contenedor") ||
            key.startsWith("dispensador") ||
            key.startsWith("recipiente") ||
            key.startsWith("tResultado") 
          );
        })
        .map((key) => {
          const estado = estados[key];
          return `${key} - Estado: ${estado.estado}`;
        });
      mostrarListaRegistros(registros);
    } else {
      mostrarMensaje("No hay registros de estados en la base de datos.");
    }
  });
  function mostrarListaRegistros(registros) {
    registros.forEach((registro) => {
      const [tipo, estado] = registro.split(" - Estado: ");
      let mensaje;
      if (estado == 0) {
        mensaje = "Cerrado";
      } else if (estado == 1) {
        mensaje = "Abierto";
      } else {
        mensaje = "Cerrado"; 
      }
      switch (tipo) {
        case "contenedor1":
          document.getElementById(
            "ContenedorAgua"
          ).textContent = `${estado}`;
          break;
        case "contenedor2":
          document.getElementById(
            "ContenedorComida"
          ).textContent = `${estado}`;
          break;
        case "dispensador1":
          document.getElementById(
            "DispensadorAgua"
          ).textContent = `${mensaje}`;
          const checkboxAgua = document.getElementById("dispensarAgua");
          if (checkboxAgua && checkboxAgua.checked !== (estado == 1)) {
            checkboxAgua.checked = (estado == 1);
          }
          break;
        case "dispensador2":
          document.getElementById(
            "DispensadorComida"
          ).textContent = `${mensaje}`;
          const checkboxComida = document.getElementById("dispensarComida");
          if (checkboxComida && checkboxComida.checked !== (estado == 1)) {
            checkboxComida.checked = (estado == 1);
          }
          break;
        case "recipiente1":
          document.getElementById(
            "RecienteAgua"
          ).textContent = `${estado}`;
          break;
        case "recipiente2":
          document.getElementById(
            "RecienteComida"
          ).textContent = ` ${estado}`;
          break;
        case "tResultado1":
          document.getElementById(
            "Resultado1"
          ).textContent = `${estado}`;
          break;
        case "tResultado2":
          document.getElementById(
            "Resultado2"
          ).textContent = `${estado}`;
          break;
        default:
          break;
      }
    });
  }



  /* mustra el el tipo y intervalo, haci como tambien esta pendiente de cualquier cambio */

  firebase.database().ref('test/estados').on('value', (snapshot) => {
    const estados = snapshot.val();
    if (estados) {
        const registrosDeTiempo = {};
        Object.keys(estados).forEach((key) => {
            if (key.startsWith("tiempo")) {
                const tiempo = estados[key];
                registrosDeTiempo[key] = {
                    intervalo: tiempo.intervalo,
                    tipo: tiempo.tipo
                };
            }
        });

        mostrarRegistrosDeTiempo(registrosDeTiempo);
    } else {
        mostrarMensaje("No hay registros de tiempo en la base de datos.");
    }
});

function mostrarRegistrosDeTiempo(registrosDeTiempo) {
    const tiempo1 = registrosDeTiempo["tiempo1"];
    const tiempo2 = registrosDeTiempo["tiempo2"];

    if (tiempo1) {
        const tipoTiempo1 = tiempo1.tipo === 'm' ? 'minuto' : tiempo1.tipo === 's' ? 'segundo' : 'desconocido';
        document.getElementById('Tiempo1').textContent = `${tiempo1.intervalo} ${tipoTiempo1}`;
    } else {
        document.getElementById('Tiempo1').textContent = `Tiempo 1: No hay información disponible`;
    }
    if (tiempo2) {
        const tipoTiempo2 = tiempo2.tipo === 'm' ? 'minuto' : tiempo2.tipo === 's' ? 'segundo' : 'desconocido';
        document.getElementById('Tiempo2').textContent = `${tiempo2.intervalo} ${tipoTiempo2}`;
    } else {
        document.getElementById('Tiempo2').textContent = `Tiempo 2: No hay información disponible`;
    }
}
      

/* agrega y mantiene el valor de tiempo de agua y comida */


function actualizarEstado(id, abierto) {
  let comando;

  if (id === 'dispensarAgua') {
    comando = abierto ? 'wd:1' : 'wd:0'; 
  } else if (id === 'dispensarComida') {
    comando = abierto ? 'fd:1' : 'fd:0'; 
  } else {
    return;
  }

  actualizarComando(comando);

  const checkbox = document.getElementById(id);
  if (checkbox) {
    checkbox.checked = abierto;
  }
}

function actualizarComando(comando) {
  firebase.database().ref('test/comando').set(comando)
    .then(() => {
      console.log(`Comando actualizado a "${comando}" exitosamente.`);
    })
    .catch((error) => {
      console.error('Error al actualizar el comando:', error);
    });
}



/* muetra el valor el valor que que se seleciona en le rango de valor */
document.addEventListener('DOMContentLoaded', () => {
  inicializarEstadoDesdeFirebase();
});

function updateRangeValue(inputRange, spanId) {
  let rangeValue = inputRange.value;
  document.getElementById(spanId).textContent = rangeValue;
}

function inicializarYActualizarRango(idInput, idSpan, referenciaFirebase) {
  const inputRange = document.getElementById(idInput);
  const spanValue = document.getElementById(idSpan);

  firebase.database().ref(referenciaFirebase).on('value', (snapshot) => {
    const valorFirebase = snapshot.val();
    if (valorFirebase !== null && !isNaN(valorFirebase)) {
      inputRange.value = valorFirebase;
      spanValue.textContent = valorFirebase; 
    }
  });
}
inicializarYActualizarRango('tiempoAgua', 'rangeValue1', 'test/estados/tiempo1/intervalo');

inicializarYActualizarRango('tiempoComida', 'rangeValue2', 'test/estados/tiempo2/intervalo');




/* ACTAULIZAR O INGRESA EL ESTADO DE TIEMPO AGUA*/

function actualizarTiempo(coleccionTiempo) {
  let intervalo;
  let tipo;

  if (coleccionTiempo === 'tiempo1') {
    intervalo = document.getElementById('tiempoAgua').value;
    tipo = document.getElementById('tipoTiempoAgua').value;
  } else if (coleccionTiempo === 'tiempo2') {
    intervalo = document.getElementById('tiempoComida').value;
    tipo = document.getElementById('tipoTiempoComida').value;
  } else {
    return; 
  }

  let comando;
  if (coleccionTiempo === 'tiempo1') {
    comando = `wdT:${intervalo}${tipo}`;
  } else if (coleccionTiempo === 'tiempo2') {
    comando = `fdT:${intervalo}${tipo}`;
  }

  actualizarComando(comando);
}

function actualizarComando(comando) {
  firebase.database().ref('test/comando').set(comando)
    .then(() => {
      console.log(`Comando actualizado a "${comando}" exitosamente.`);
    })
    .catch((error) => {
      console.error('Error al actualizar el comando:', error);
    });
}

function updateRangeValue(inputRange, spanId) {
  const rangeValue = inputRange.value;
  document.getElementById(spanId).textContent = rangeValue;
}


/* consulta y filtrados */
function mostrarDatosEnTabla() {
  const ref = firebase.database().ref("test/registros");
  ref.on("value", (snapshot) => {
    const tableBody = document.getElementById("tablaRegistros");
    tableBody.innerHTML = ""; 

    snapshot.forEach((childSnapshot) => {
      const registro = childSnapshot.val();
      const { idComponente, estado,tiempo } = registro;

      let nombre = "";
      if (idComponente === 1) {
        nombre = "Agua";
      } else if (idComponente === 2) {
        nombre = "Comida";
      } else {
        nombre = "Desconocido";
      }

      const newRow = document.createElement("tr");

      newRow.innerHTML = `
        <td>${nombre}</td>
        <td>${tiempo}</td>
        <td>${estado}</td>
      `;

      tableBody.appendChild(newRow);
    });
  });
}

mostrarDatosEnTabla();

document.getElementById("filter-button").addEventListener("click", () => {
  const categoryFilter = document.getElementById("filter-category").value;
  const statusFilter = document.getElementById("filter-status").value;

  const ref = firebase.database().ref("test/registros");
  ref.on("value", (snapshot) => {
    const tableBody = document.getElementById("tablaRegistros");
    tableBody.innerHTML = ""; 

    snapshot.forEach((childSnapshot) => {
      const registro = childSnapshot.val();
      const { idComponente, estado,tiempo } = registro;

      let nombre = "";
      if (idComponente === 1) {
        nombre = "Agua";
      } else if (idComponente === 2) {
        nombre = "Comida";
      } else {
        nombre = "Desconocido";
      }

      if ((categoryFilter === "all" || nombre.toLowerCase() === categoryFilter) &&
          (statusFilter === "all" || estado.toLowerCase() === statusFilter)) {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
          <td>${nombre}</td>
          <td>${tiempo}</td>
          <td>${estado}</td>
        `;
        tableBody.appendChild(newRow);
      }
    });
  });
});
