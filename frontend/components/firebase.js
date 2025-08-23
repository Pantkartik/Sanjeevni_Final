// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBybfYZpgCoi8S6y_GQsNtE961yMm8SJ2M",
  authDomain: "sanjeevni-b96da.firebaseapp.com",
  projectId: "sanjeevni-b96da",
  storageBucket: "sanjeevni-b96da.firebasestorage.app",
  messagingSenderId: "151957907651",
  appId: "1:151957907651:web:4ec3092861a4fd24875a76"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app);

export default app;