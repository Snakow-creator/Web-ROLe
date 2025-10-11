import { useState } from "react";
import api from "../api";
import Button from "../components/Button";


function InputPassword({name, placeholder, value, onChange}) {
  const [showPassword, setShowPassword] = useState(false);

  const handleShowPassword = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div>
      <span className="w-full relative">
        <input
          type={ showPassword ? "text" : "password"}
          name={ name }
          placeholder={ placeholder } // placeholder
          value={ value }
          minLength="8"
          maxLength="20"
          onChange={ onChange }
          className="border rounded px-1 py-0.5"/>
          <button
              type="button"
              onClick={ handleShowPassword }
              className="absolute right-2 translate-y-1 h-full text-gray-600 pointer font-bold text-2xl rounded-full"
              >*
          </button>
      </span>
    </div>
  )
}

export default function Register() {
  const [formData, setFormData] = useState({
    name: "",
    password1: "",
    password2: ""
  })

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/register", formData)
      console.log(response);

    } catch (error) {
      console.error(error);
    }
  }


  return (
    <>
      <h1 className="text-3xl font-extrabold">Регистрация</h1>

      <form onSubmit={ handleSubmit } className="mt-2">
          <input
            type="text"
            placeholder="Ник"
            className="block border rounded px-1 py-0.5"
            name="name"
            value={ formData.name }
            onChange={ handleChange }
          />

          <InputPassword
            name="password1"
            placeholder="Пароль"
            value={ formData.password1 }
            onChange={ handleChange }/>

          <InputPassword
            name="password2"
            placeholder="Подтвердите пароль"
            value={ formData.password2 }
            onChange={ handleChange }/>

          <Button type="submit">Зарегистрироваться</Button>
      </form>
    </>
  );
}
