import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';

import { logout, getAuth } from '../services/apiService/auth';
import logo from '/logo.png' // пока не трогаем

export default function Header() {
  const [bar, setBar] = useState(<></>);
  const [auth, setAuth] = useState(null);

  const checkAuth = async () => {
    const res = await getAuth();
    setAuth(res.auth);
    console.log(res)
  }

  const logoutUser = async () => {
    const setAuthFalse = () => {
      setAuth(false);
    }

    await logout(setAuthFalse);
  }



  const handleAuth = () => {
    if (auth) {
      setBar(
        <>
          <h3><Link to="/profile" className='font-bold'>профиль</Link></h3>
          <h3><Link to="/add/task" className="font-bold">добавить задачу</Link></h3>
          <h3><Link to="/tasks" className='font-bold'>мои задачи</Link></h3>
          <h3><Link to="/items" className='font-bold'>магазин</Link></h3>
          <h3><button className='cursor-pointer font-bold' onClick={logoutUser}>выйти</button></h3>
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
  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    handleAuth();
  }, [auth]);

  return (
    <header>
      <div className="flex ml-4 space-x-8">
        <Link to="/">
          <img className='w-[180px] h-[60px] py-2' src={logo} alt={"Realms Of Life"} />
        </Link>
        {bar}
      </div>
      <hr />
    </header>
  );
}
