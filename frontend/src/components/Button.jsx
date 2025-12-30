export default function Button ({
  children, onClick, type, disabled=true
}) {
  return (
    <button
      className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
      onClick={onClick}
      type={type}>
      {children}
    </button>
  );
}
