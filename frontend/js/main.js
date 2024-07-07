import { Welcome } from "./Welcome.js";

const location = window.location;
console.log(location);

const welcomeHeader = document.querySelector(".welcome__text");
const welcome = new Welcome(welcomeHeader);

const { hours } = welcome.getTimeOfDay();

if (hours >= 17) {
  welcomeHeader.textContent = "Dobry wieczór!";
}

welcome.tester();