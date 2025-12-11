const message = [
  "Недельная норма выполнена, поздравляем!",
  "Ай красава! Разъебал эту неделю!",
  "Неделя уничтожена, но не все лишнее убило!",
]

export default function getWeeklyMessage() {
  return message[Math.floor(Math.random() * message.length)] + "\nБонус: 150 Spoints, 150 Xp, увеличены множители."
}
