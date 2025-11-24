import { useParams } from 'react-router-dom';

export default function ThreadDetailPage() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Thread Detail</h1>
      <p className="text-gray-600">Thread ID: {id}</p>
    </div>
  );
}
