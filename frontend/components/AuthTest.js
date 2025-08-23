import { auth } from './firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';

export function testAuth() {
  console.log('Testing Firebase Auth configuration...');
  console.log('Auth object:', auth);
  console.log('Auth app:', auth.app);
  console.log('Auth config:', auth.app.options);
  
  return {
    auth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword
  };
}
