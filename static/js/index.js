var typingSpeed = 5; // ms
var fontSize = Number(getComputedStyle(document.documentElement).getPropertyValue('--fontSize').slice(0, -2));

var commandPromptLineStart = "\nlyagva@frogame:", commandPromptLineEnd = "$ ";
var resultText = "      :::::::::: :::::::::   ::::::::   ::::::::      :::       :::   :::   ::::::::::\n     :+:        :+:    :+: :+:    :+: :+:    :+:   :+: :+:    :+:+: :+:+:  :+:\n    +:+        +:+    +:+ +:+    +:+ +:+         +:+   +:+  +:+ +:+:+ +:+ +:+\n   :#::+::#   +#++:++#:  +#+    +:+ :#:        +#++:++#++: +#+  +:+  +#+ +#++:++#\n  +#+        +#+    +#+ +#+    +#+ +#+   +#+# +#+     +#+ +#+       +#+ +#+\n #+#        #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#       #+# #+#\n###        ###    ###  ########   ########  ###     ### ###       ### ##########\n" +
                 "Hello! Welcome to our site!\n" +
                 "Type \"help\" to get commands list\n" +
                 "Use \"info\" to get information about this site\n\n" +
                 "Made by Lyagva\n";
var currentIndex = 0;

var outputField = document.getElementById("outputField");
var heightFiller = document.getElementById("heightFiller");

var foregroundColors = ["#FFFFFF", "#800000", "#008000", "#808000",
                        "#000080", "#800080", "#008080", "#C0C0C0",
                        "#808080", "#FF0000", "#00FF00", "#FFFF00",
                        "#0000FF", "#FF00FF", "#00FFFF", "#FFFFFF"]
var root = document.querySelector(":root");
var updateInstant = false;

var path = "";
var mode = "terminal";


var body = document.body; body.addEventListener("keydown", onKeyDown);

var allowedChars = " qwertyuiop[]asdfghjkl;'zxcvbnm,./<>?\":{}1234567890-=!@#$%^&*()_+~"
var canType = false;
var promptHistory = []; var historySelectedIndex = 0; var currentPrompt = "";

var audioSource = document.getElementById("audioSource");
var audioSrc = "";


if (getCookie("skipIntro") == "true") {
    updateText(instant=true);
}

setInterval(updateText, typingSpeed);
changeColor();
addCommandOutput("");


function updateText(instant = false) {
    heightFiller.style.height = (window.innerHeight - fontSize * 3 / 2).toString() + "px";

    updateInstant = false;
    if (mode === "rain") { updateInstant = true; updateRain(); }

    if (instant || updateInstant) {
        outputField.textContent = resultText;
        currentIndex = resultText.length;
        return;
    }

    if (outputField.textContent.length >= resultText.length)
    {
    canType = true;
    return;
    }
    canType = false;
    outputField.textContent += resultText[currentIndex];
    currentIndex += 1;
}

function onKeyDown(event) {
    if (event.key === " ") {event.preventDefault(); }
    if (!canType) { return; }

    if (event.key === "Enter") {
        event.preventDefault();
        if (mode === "terminal") {
            sendInput(); return;
        } else if (mode === "rain") {
            mode = "terminal";
            changeMode(mode);
        }
        return;
    }

    if (mode === "rain") { return; }

    if (event.key === "Backspace") { onBackspace(); return; }
    if (event.key === "ArrowUp") { onArrowUp(); event.preventDefault(); return; }
    if (event.key === "ArrowDown") { onArrowDown(); event.preventDefault(); return; }
    if (event.ctrlKey) { ctrlActions(event); return; }

    char = event.key.toLowerCase();
    if (!allowedChars.includes(char)) { return; } // Check for blocked char

    resultText += char;
currentPrompt += char;
}

function onBackspace() {
  if (currentPrompt.length == 0) { return; }
  resultText = resultText.slice(0, -1); currentPrompt = currentPrompt.slice(0, -1);
  currentIndex--; currentPrompt.length--; 
  updateText(instant=true);
}

async function ctrlActions(event) {
  if (event.key == "v") {
    try {
      clipboardText = await navigator.clipboard.readText();
    } catch (err) {}

    resultText += clipboardText;
    currentPrompt += clipboardText;
  }
}

function sendInput() {
  sendData();

  if (currentPrompt != "") {
    promptHistory.push(currentPrompt); historySelectedIndex = promptHistory.length;
  }
  
  currentPrompt.length = 0;
  currentPrompt = "";
}

function addCommandOutput(text) {
    pathText = "~";
    if (path != "") { pathText = path; }

    resultText += "\n" + text + commandPromptLineStart + pathText + commandPromptLineEnd;

}

function onArrowUp() {
  if (historySelectedIndex <= 0) { return; }
  historySelectedIndex--;
  updateAfterArrowOperations();
}

function onArrowDown() {
  if (historySelectedIndex >= promptHistory.length - 1) { return; }
  historySelectedIndex++;
  updateAfterArrowOperations();
}

function updateAfterArrowOperations() {
  resultText = resultText.slice(0, resultText.length - currentPrompt.length);
  updateText(instant=true);

  currentPrompt = promptHistory[historySelectedIndex];

  resultText += currentPrompt;
}

function sendData() {
  data = {"prompt": currentPrompt,
          "path": path,
          "audioSrc": audioSrc,
          "audioDuration": audioSource.duration.toString(),
          "audioPlayback": audioSource.currentTime.toString()};

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/sendPrompt", true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  xhr.send(JSON.stringify(data));

  xhr.onloadend = function () {
    onDataGet(xhr);
  };
}

function onDataGet(xhr) {
    resultJson = JSON.parse(xhr.responseText);

    document.cookie = resultJson["cookie"];
    changeColor();

    if (resultJson["cls"]) { clear(); }

    path = resultJson["path"];
    if (resultJson["audioPath"]) {
        audioSrc = resultJson["audioPath"];
        audioSource.src = audioSrc;
    }
    if (resultJson["audioVolume"] != "") {
        audioSource.volume = +(resultJson["audioVolume"]);
    }
    if (resultJson["audioLoop"]) {
        if (resultJson["audioLoop"] === "true") { audioSource.loop = true; }
        else { audioSource.loop = false; }
    }
    if (resultJson["audioState"] === "play") { audioSource.play(); }
    if (resultJson["audioState"] === "pause") { audioSource.pause(); }
    if (resultJson["audioState"] === "stop") { audioSource.pause(); audioSource.currentTime = 0;}
    if (resultJson["audioPlayback"] != "") {
        audioPlayback = Number(resultJson["audioPlayback"]);
        audioSource.currentTime = audioPlayback;
    }

    if (resultJson["mode"]) { mode = resultJson["mode"]; }

    addCommandOutput(resultJson["resultText"]);
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function changeColor() {
    colorIndex = getCookie("color");
    if (colorIndex === "") { colorIndex = 10; document.cookie = "color=" + colorIndex; }
    root.style.setProperty("--foreground", foregroundColors[colorIndex]);
}

function clear() {
    resultText = "";
    currentPrompt = "";
    updateText(instant=true);
}

function changeMode() {
    if (mode === "terminal") {
        clear(); addCommandOutput("");
    }
}

String.prototype.replaceAt = function(index, replacement) {
    return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

var rainMatrix = [];
var rainWidth = Math.floor(window.innerWidth / (fontSize * 3 / 4)),
    rainHeight = Math.floor(window.innerHeight / (fontSize * 3 / 4) * 9 / 16) - 5,
    rainTickTimeout = 15, rainTick = 0, rainDropsAtTick = 2, rainRandomTickShortens = 4,
    rainSpawningTickTimeout = 2, rainSpawningTick = 0, rainCharRange = 3;
var rainChars = " .'`^,:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$";


for (let y = 0; y < rainHeight; y++) {
    rainMatrix.push([]);
    for (let x = 0; x < rainWidth; x++) {
        rainMatrix[y].push(0);
    }
}

function updateRain() {
    rainTick++;
    if (rainTick % rainTickTimeout != 0) { return; }

    rainMatrix.pop();
    rainMatrix.unshift([...rainMatrix[0]]);

    for (let x = 0; x < rainWidth; x++) {
        rainMatrix[0][x] -= Math.ceil(Math.random() * rainRandomTickShortens);
        if (rainMatrix[0][x] < 0) { rainMatrix[0][x] = 0; }
    }

    rainSpawningTick++;
    if (rainSpawningTick % rainSpawningTickTimeout == 0) {
        for (let i = 0; i < rainDropsAtTick; i++) {
            let index = Math.floor(Math.random() * rainWidth);
            rainMatrix[0][index] = rainChars.length - 1;
        }
    }

    let rainText = "";
    for (let y = 0; y < rainHeight; y++) {
        for (let x = 0; x < rainWidth; x++) {
            charIndex = rainMatrix[y][x];
            if (charIndex != 0) {
                charIndex += -rainCharRange + Math.floor(Math.random() * 2 * rainCharRange);
                if (charIndex <= 0) { charIndex = 0; }
                if (charIndex >= rainChars.length) { charIndex = rainChars.length - 1; }
            }
            rainText += rainChars[charIndex];
        }
        rainText += "\n";
    }
    resultText = rainText + "\n\nPress Enter to Exit... ";
}
