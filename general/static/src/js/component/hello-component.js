export const HelloComponent = (text) => {
  const div = document.createElement('div');
  div.textContent = text;
  return div;
}

// Инициализация
const holder = document.querySelector('#helloWord');

if (holder) { // Всегда проверяем существование элемента!
  holder.append(HelloComponent('Hello World'));
}