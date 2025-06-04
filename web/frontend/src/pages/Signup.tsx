import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/api';

export default function Signup() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const ok = await signup(email, password, name);
    if (ok) {
      navigate('/login');
    }
  }

  return (
    <main>
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <label>Email<input value={email} onChange={e => setEmail(e.target.value)} /></label>
        <label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} /></label>
        <label>Name<input value={name} onChange={e => setName(e.target.value)} /></label>
        <button type="submit">Create Account</button>
      </form>
    </main>
  );
}
