export default function Button (props) {
  return (
    <button
      className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
      onClick={props.onClick}
      type={props.type}>
      {props.children}
    </button>
  );
}
