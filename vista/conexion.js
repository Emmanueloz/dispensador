
// https://firebase.google.com/docs/web/setup#available-libraries

const firebaseConfig = {
  apiKey: "AIzaSyA3akoe2nlqOhW5zE0rTc2Elbvv7_Ygx1g",
  authDomain: "applot-ac1bf.firebaseapp.com",
  databaseURL: "https://applot-ac1bf-default-rtdb.firebaseio.com",
  projectId: "applot-ac1bf",
  storageBucket: "applot-ac1bf.appspot.com",
  messagingSenderId: "609939820038",
  appId: "1:609939820038:web:7179c8066dc7d28e97bd87"
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
  firebase.database().ref('articles').once('value')
    .then((snapshot) => {
      const articles = snapshot.val();
      if (articles) {
        const articleKeys = Object.keys(articles);
        const articleList = articleKeys.map((key) => {
          return `${key}: ${articles[key].title}`;
        });
        mostrarListaArticulos(articleList);
      } else {
        mostrarMensaje("No hay artículos en la base de datos.");
      }
    })
    .catch((error) => {
      console.error("Error al obtener datos de Firebase:", error);
      mostrarMensaje("¡Error al obtener datos de Firebase!");
    });
}

function mostrarListaArticulos(articleList) {
  alert(`Artículos en la base de datos:\n\n${articleList.join('\n')}`);
}

function mostrarMensaje(message) {
  alert(message);
}

initializeFirebase();

consultarRegistros();