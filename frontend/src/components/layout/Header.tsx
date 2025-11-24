import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link to={ROUTES.HOME} className="text-2xl font-bold text-blue-600">
            Modern Board
          </Link>
          <div className="flex gap-4">
            <Link
              to={ROUTES.HOME}
              className="text-gray-700 hover:text-blue-600"
            >
              Home
            </Link>
            <Link
              to={ROUTES.CREATE_THREAD}
              className="text-gray-700 hover:text-blue-600"
            >
              Create Thread
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
