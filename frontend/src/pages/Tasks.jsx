import { useState, useEffect } from "react";

import { getTasks, completeTask, uncompleteTask, deleteTask } from "../services/apiService/tasks";

import { getMessageTask, getMessageLevel, getWeeklyMessage } from "../hooks/messages";
import { quests_types } from "../hooks/data"


function Task(creds) {
  const [message, setMessage] = useState('');
  const [weeklyMessage, setWeeklyMessage] = useState('');
  const [spointsLevel, setSpointsLevel] = useState('');
  const [userData, setUserData] = useState({
    spoints: 0,
    xp: 0,
    isDone: false
  });

  const onError = async (error) => {
    console.error(error);
    setMessage("Что-то пошло не так");
  }

  const submitTask = async () => {
    const onCompleteTask = async (res) => {
      if (res.data?.isUpLevel) {
        setMessage(getMessageLevel());
        setSpointsLevel(res.data.spointsLevel)
      } else {
        setMessage(getMessageTask());
      }

      if (res.data?.isWeekly) {
        setWeeklyMessage(getWeeklyMessage());
      }

      // finally logics
      setUserData({
        spoints: res.data.points,
        xp: res.data.xp,
        isDone: true
      });
    }

    await completeTask({
      id: creds.id,
      onCompleteTask: onCompleteTask,
      onError: onError
    })
  }

  const unSubmitTask = async () => {
    const onUncompleteTask = async () => {
      setMessage("Вы вернули задачу");
      setSpointsLevel('')
      setUserData({
        spoints: 0,
        xp: 0,
        isDone: false
      })
    }

    await uncompleteTask({
      id: creds.id,
      onUncompleteTask: onUncompleteTask,
      onError: onError
    })
  }

  const delTask = async () => {
    const onDeleteTask = async (title) => {
      setMessage(`Задача ${title} успешно удалена`);
      setUserData(prev => ({
        ...prev,
        isDone: false
      }))
    }

    await deleteTask({
      id: creds.id,
      onDeleteTask: onDeleteTask,
      onError: onError
    })
  }

  return (
    <div>
      <p className="font-bold text-lg">
        {creds.index + 1}. {creds.title}
      </p>
      <p>
        Тип задания: <b>{quests_types[creds.type]}</b>
      </p>
      {creds.description &&
        <p className="mt-1 font-mono">{creds.description}</p>
      }

      {message && <p className="font-medium">{message}</p>}

      <div className="space-y-1">
        {userData.xp > 0 && userData.spoints > 0 &&
          <>
            <p>Награда: <b>+{userData.spoints} Spoints +{userData.xp} Xp</b> </p>
          </>}
        {spointsLevel && <p>Уровень повышен, награда: <b>+{spointsLevel} Spoints</b></p>}
      </div>

      {weeklyMessage && <p className="font-medium">{weeklyMessage}</p>}

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
            onClick={delTask}
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
    const onFinish = (data) => {
      setTasks(data);
    }

    getTasks({ onFinish });
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
