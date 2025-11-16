import Button from "../components/Button";
import { useState, useEffect, use } from "react";
import getAuth from "../hooks/checkAuth";
import api from "../api";


export default function Login() {
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
      const res = await api.post("/login", formData)
      window.location.href = "/";
    } catch (error) {
      console.error(error);
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
            autoComplete="off"
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

        <Button type="submit">Вход</Button>
      </form>
    </>
  );
}
