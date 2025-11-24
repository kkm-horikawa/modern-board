import { Link } from 'react-router-dom';
import { ROUTES } from '@/constants/routes';

export default function NotFoundPage() {
  return (
    <div className="container mx-auto px-4 py-8 text-center">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <p className="text-xl text-gray-600 mb-8">Page not found</p>
      <Link
        to={ROUTES.HOME}
        className="text-blue-600 hover:text-blue-800 underline"
      >
        Go back to home
      </Link>
    </div>
  );
}
