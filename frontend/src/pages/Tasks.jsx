import api from "../api";
import { useState, useEffect } from "react";

function Task({index, title, description, type}) {
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
