import Button from "../components/Button";
import { useState } from "react";
import { addTask } from "../services/apiService/tasks";
import { quests_types } from "../hooks/data"



export default function AddTask() {
  const [message, setMessage] = useState('');
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    type: "",
    date: new Date().toISOString().split('T')[0],
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      setMessage("Введите заголовок");
      return;
    }
    if (!formData.type) {
      setMessage("Выберите тип задачи");
      return;
    }

    const res = await addTask(formData);
    console.log(res);
    setMessage(res.status === 200
      ? `Задача ${formData.title} сложности "${quests_types[formData.type]}" успешно создана`
      : "Ошибка при создании задачи"
    );
  };

  function Radio({ children, value }) {
    return (
      <span className="flex">
        <input
          type="radio"
          className="mt-2 p-3"
          name="type"
          id={value}
          value={value}
          onChange={handleChange}
          checked={formData.type === value}
        />
        <label
          htmlFor={value}
          className="mt-auto ml-1">
          {children}
        </label>
      </span>
    )
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="mt-2">
        <input
          type="text"
          className="block border rounded px-1 py-0.5"
          placeholder="Заголовок"
          name="title"
          value={formData.title}
          onChange={handleChange}
        />
        <input
          type="text"
          className="block border rounded px-1 py-0.5"
          placeholder="Описание"
          name="description"
          value={formData.description}
          onChange={handleChange}
        />
        <Radio value="simple">Простые</Radio>
        <Radio value="common">Обычные</Radio>
        <Radio value="hard">Трудные</Radio>
        <Radio value="expert">Сложные</Radio>
        <Radio value="hardcore">Хардкор</Radio>

        <label htmlFor="createDate" className="block font-bold">
          Дата запланированного квеста
        </label>
        <input type="date"
          id="createDate"
          name="date"
          className="rounded-md border p-1"
          value={formData.date}
          onChange={handleChange} />

        <Button type="submit">Создать</Button>
      </form>
      {message && <p className="text-green-500 mt-2">{message}</p>}
    </>
  )
};
