import { Link } from 'react-router-dom';
import logo from '/logo.png' // пока не трогаем

export default function Header() {
  return (
    <header>
      <div className="flex ml-4 space-x-8">
        <Link to="/">
          <img className='w-[180px] h-[60px] py-2' src={ logo } alt={"Realms Of Life"} />
        </Link>
        <h3><Link to="/login" className='font-bold'>войти</Link></h3>
        <h3><Link className='font-bold'>меню</Link></h3>
      </div>
      <hr />
    </header>
  );
}
