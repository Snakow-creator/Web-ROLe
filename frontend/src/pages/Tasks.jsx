import api from "../api";
import { useState, useEffect } from "react";
import getMessage from "../hooks/getMessage";
import getMessageLevel from "../hooks/getMessageLevel";
import { getCSRFCookie } from "../hooks/getCookies";


function Task({id, index, title, description, type}) {
  const [message, setMessage] = useState('');
  const [spointsLevel, setSpointsLevel] = useState('');
  const [userData, setUserData] = useState({
    spoints: 0,
    xp: 0,
    isDone: false
  });

  const submitTask = async () => {
    const CSRFToken = getCSRFCookie();
    try {
      const res = await api.put(`/complete/task/${id}`, {}, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": CSRFToken
        }
      });
      if (res.data?.up_level) {
        setMessage(getMessageLevel());
        setSpointsLevel(res.data.spoints_level)
      } else {
        setMessage(getMessage());
      } // finally logics
      setUserData({
        spoints: res.data.points,
        xp: res.data.xp,
        isDone: true
      });

    } catch (error) {
      console.error(error);
      setMessage("Что-то пошло не так");
    }
  }

  const unSubmitTask = async () => {
    const CSRFToken = getCSRFCookie();
    try {
      const res = await api.put(`/uncomplete/task/${id}`, {}, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": CSRFToken
        }
      });
      setMessage("Вы вернули задачу");
      setSpointsLevel('')
      setUserData({
        spoints: 0,
        xp: 0,
        isDone: false
      })
    } catch (error) {
      console.error(error);
      setMessage("Что-то пошло не так");
    }
  }

  const deleteTask = async () => {
    const CSRFToken = getCSRFCookie();
    try {
      await api.delete(`/delete/task/${id}`, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": CSRFToken
        }
      });
      setMessage("Задача успешно удалена");
      setUserData(prev => ({
        ...prev,
        isDone: false
      }))
    } catch (error) {
      console.error(error)
      setMessage("Что-то пошло не так");
    }
  }

  return (
    <div>
      <p className="font-bold text-lg">
        { index+1 }. { title }
      </p>
      <p>
        Тип задания <b>{ type }</b>
      </p>
      {description &&
       <p className="mt-1 font-mono">{ description }</p>
      }

      {message && <p className="font-medium">{ message }</p>}

      <div className="space-y-1">
        {userData.xp > 0 && userData.spoints > 0 &&
        <>
          <p>тест</p>
          <p>Награда: <b>+{ userData.spoints } Spoints +{ userData.xp } Xp</b> </p>
        </>}
        {spointsLevel && <p>Уровень повышен, награда: <b>+{ spointsLevel } Spoints</b></p>}
      </div>

      {!userData.isDone ? (
        <>
          <button
            className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
            onClick={submitTask}
            type='button'>
            Сделано
          </button>
          <button
            className="block mt-2 bg-red-500 px-1 rounded-md border border-black"
            onClick={deleteTask}
            type='button'>
            Удалить
          </button>
        </>
      ) : (
        <button
          className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
          onClick={unSubmitTask}
          type='button'>
          Вернуть
        </button>
      )
      }
    </div>
  )
}

export default function Tasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await api.get("/tasks");
        setTasks(res.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchTasks();
  }, []);

  return (
    <>
      <h1 className="text-2xl font-extrabold">Мои задачи</h1>
      <div className="space-y-4">
        {tasks.map((task, index) => (
          <Task
            key={task._id}
            id={task._id}
            index={index}
            title={task.title}
            description={task.description}
            type={task.type}
          />
        ))}
      </div>
    </>
  );
}
