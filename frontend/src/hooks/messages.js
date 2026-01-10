import { messageTask, messageUpLevel, messageWeeklyBonus } from "../data/messageData"


export function getMessageTask() {
  return messageTask[Math.floor(Math.random() * messageTask.length)]
}

export function getMessageLevel() {
  return messageUpLevel[Math.floor(Math.random() * messageUpLevel.length)]
}

export function getWeeklyMessage() {
  return messageWeeklyBonus[Math.floor(Math.random() * messageWeeklyBonus.length)] + "\nБонус: 150 Spoints, 150 Xp, увеличены множители."
}
