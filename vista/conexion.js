
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
try {
    firebase.initializeApp(firebaseConfig);
    console.log("Firebase connected successfully!");
    alert("¡Conexión exitosa a Firebase!");
} catch (error) {
    console.error("Error connecting to Firebase:", error);
    alert("¡Error al conectar a Firebase!");
}