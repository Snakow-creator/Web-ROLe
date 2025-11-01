const message = [
  "Уровень повышен",
  "Ты не только задачу уничтожил, но и уровень повысил? Четко братан",
  "Уровень повысился, ты красавчик!",
  "Уровень повысился, чуешь мощь?",
  "ВААААААЙ БРАТ ТЫ ЧТО УРОВЕНЬ ПОВЫСИЛ? ДА ТЫ АХУЕНЕН БРАТАН"
]

export default function getMessageLevel() {
  return message[Math.floor(Math.random() * message.length)]
}
