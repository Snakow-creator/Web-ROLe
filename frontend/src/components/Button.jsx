export default function Button ({children, onClick}) {
  return (
    <button
      className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
      type="submit">
      {children}
    </button>
  );
}
