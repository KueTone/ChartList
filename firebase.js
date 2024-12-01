// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAMasYh4_F3mCVeuiDvIUso3xnjVl7RHJY",
  authDomain: "inventory-1b43e.firebaseapp.com",
  projectId: "inventory-1b43e",
  storageBucket: "inventory-1b43e.appspot.com",
  messagingSenderId: "385558110958",
  appId: "1:385558110958:web:a9e3b6d4bb2c1bc4ab89ff",
  measurementId: "G-M35TXRGJVX",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);
export { firestore };
