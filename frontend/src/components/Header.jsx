import { Link } from 'react-router-dom';
import logo from '/logo.png' // пока не трогаем
import { useState } from 'react';
import { useEffect } from 'react';
import api from '../api';

export default function Header(auth_user) {
  const [bar, setBar] = useState();
  const [auth, setAuth] = useState(auth_user);

  function logout() {
    api.post("/logout");
    setAuth(false);
    handleAuth();
  }

  useEffect(() => {
    const handleAuth = () => {
      if (auth) {
        setBar(
          <>
            <h3><Link to="/profile" className='font-bold'>профиль</Link></h3>
            <h3><button className='cursor-pointer font-bold' onClick={ logout }>выйти</button></h3>
          </>
        )
      } else {
        setBar(
          <>
            <h3><Link to="/login" className='font-bold'>войти</Link></h3>
            <h3><Link to="/register" className='font-bold'>регистрация</Link></h3>
          </>
        )
      }
    }
    handleAuth();
  }, []);

  return (
    <header>
      <div className="flex ml-4 space-x-8">
        <Link to="/">
          <img className='w-[180px] h-[60px] py-2' src={ logo } alt={"Realms Of Life"} />
        </Link>
        { bar}
      </div>
      <hr />
    </header>
  );
}
