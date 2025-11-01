import api from "../api";
import { useState, useEffect } from "react";
import getMessage from "../hooks/getMessage";
import getMessageLevel from "../hooks/getMessageLevel";
import { getCSRFCookie } from "../hooks/getCookies";


function Task({id, index, title, description, type}) {
  const [message, setMessage] = useState('');
  const [isDone, setIsDone] = useState(false);

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
        } else {
          setMessage(getMessage());
        }
        setIsDone(true);

      } catch (error) {
        console.error(error);
        setMessage("Что-то пошло не так");
      }
  }
  return (
    <div>
      <p>
        { index+1 }. <b>{ title }</b>
      </p>
      <p>
        Тип задания <b>{ type }</b>
      </p>
      {description &&
       <p className="mt-1 font-mono">{ description }</p>
      }

      {message && <p>{ message }</p>}

      {!isDone &&
        <button
          className="block mt-2 bg-gray-200 px-1 rounded-md border border-gray-600"
          onClick={submitTask}
          type='button'>
          Сделано
        </button>
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
        console.log(res.data);
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
