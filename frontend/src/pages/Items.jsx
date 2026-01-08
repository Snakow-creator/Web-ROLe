import Button from "../components/Button";
import { useState, useEffect } from "react";
import { fetchBuyItem, fetchItems } from "../services/apiService/items";
import { useRef } from "react";


function Item({ id, index, title, description, price, type }) {
  const [message, setMessage] = useState('');
  const counter = useRef({});

  const purchaseItem = async () => {
    const res = await fetchBuyItem(id);
    const title = res.data.title;

    if (!counter.current[title]) {
      counter.current[title] = 0;
    }

    counter.current[title]++;

    if (counter.current[title] > 1) {
      setMessage(`${res.data.message} x${counter.current[title]}`);
    } else {
      setMessage(res.data.message);
    }

  }

  return (
    <div>
      <p className="font-bold text-lg">
        {index}. {title}
      </p>

      <p className="font-bold">
        Тип: {type}
      </p>

      <p className="font-sans">{description}</p>

      <p>
        Цена: {price}
      </p>

      {message && <p>{message}</p>}

      <Button
        onClick={purchaseItem}
        type='button'>
        Приобрести
      </Button>
    </div>
  )
}

export default function Items() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const setCurrentItems = (data) => {
      setItems(data);
    }

    fetchItems(setCurrentItems);
  }, []);

  return (
    <>
      <h1 className="text-2xl font-extrabold">Магазин услуг</h1>
      <div className="space-y-4">
        {items.map((item, index) => (
          <Item
            key={item._id}
            id={item._id}
            index={index + 1}
            title={item.title}
            description={item.description}
            price={item.price}
            type={item.type}
          />
        ))}
      </div>
    </>
  );
}
