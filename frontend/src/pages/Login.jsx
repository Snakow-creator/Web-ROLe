import Button from "../components/Button";
import { useState } from "react";
import api from "../api";

function P({children}) {
  return (
    <p className="mt-0.5">
      {children}
    </p>
  );
}

export default function Login() {
  const [message, setMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    password: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/login", formData)

      console.log(response);
      setMessage (
        <>
          <h1 className="">
            Вход выполнен
          </h1>
            <P>Добро пожаловать, <b>{ response.data.name }</b></P>
            <P>Ваш уровень: <b>{ response.data.level }</b></P>
            <P>Ваш опыт: <b>{ response.data.xp }</b></P>
        </>
      );
    } catch (error) {
      console.error(error);
      setMessage(
        <>
        <h1>Ошибка</h1>
        </>
      )
    }
  }

  const handleShowPassword = () => {
    setShowPassword(!showPassword);
  }

  return (
    <>
      <h1 className="text-3xl font-bold">Войти в аккаунт</h1>

      <form onSubmit={handleSubmit} className="mt-2">
        <input
          type="text"
          id="name"
          name="name"
          autoComplete={true}
          placeholder="Ник"
          value={ formData.name }
          onChange={ handleChange }
          className="block border rounded px-1 py-0.5" />

        <span className="w-full relative">
          <input
            type={ showPassword ? "text" : "password" }
            id="password"
            name="password"
            placeholder="Пароль"
            value={ formData.pword }
            minLength="8"
            maxLength="20"
            onChange={ handleChange }
            className="border rounded px-1 py-0.5"/>
            <button
                type="button"
                onClick={ handleShowPassword }
                className="absolute right-2 translate-y-1 h-full text-gray-600 pointer font-bold text-2xl rounded-full"
                >*
            </button>
          </span>

        <Button>Вход</Button>
      </form>

      <div>
        { message }
      </div>
    </>
  );
}
