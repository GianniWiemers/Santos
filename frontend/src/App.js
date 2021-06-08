import Loading from './components/loading'
import Header from './components/header'
import Home from './components/home'
import QuestionsPage from './components/questionsPage'
import AnswerPage from './components/answerPage'
import EliminationPage from './components/eliminationPage'
import GuessPage from './components/guessPage'
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client'

const socket = io.connect("http://127.0.0.1:5000/")

const App = () => {
  

  const [gameState, setgameState] = useState(0);
  const [toSend, settoSend] = useState("wait");
  const [timer, settimer] = useState(100);
  const [images, setimages] = useState([]);
  const [questions, setquestions] = useState([]);
  const [selection, setselection] = useState([]);
  const [guessImage, setguessImage] = useState([]);
  const [answer, setanswer] = useState(0);
  const [questionId, setquestionId] = useState(0);
  const [textLabel, settextLabel] = useState("");
  const [oppQuestion, setoppQuestion] = useState("no opponent question");
  const [oppimg, setoppimg] = useState('https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png');
  const [loadingMessage, setloadingMessage] = useState("Searching for another player...")
  const [timedState, settimedState] = useState(false);

  function updateTimer() {
    if(timer <= 0) {
      roundDone()
    } else {
      settimer(timer - 0.1)
    }
  }

  function roundDone() {
    console.log("round done")
    emitToSocket();
    setloadingMessage("Waiting for server...")
    setgameState(1);
    settimer(100);
    settimedState(false);
  }

  function askQuestion(question, textArea) {
    setloadingMessage("Waiting for opponent...")
    setgameState(1)
    setquestionId(question)
    settextLabel(textArea)
  }

  function toGuessPage(toPage) {
    if(toPage === true) {
      setgameState(6)
    } else {
      setgameState(3)
    }
  }

  function guessTheImage() {
    setloadingMessage("Waiting for opponent...")
    setgameState(1)
    settoSend("send_guess")
  }

  function answerQuestion(answerId) {
    setloadingMessage("Waiting for opponent...")
    setgameState(1)
    setanswer(answerId)
  }

  function emitToSocket() {
    switch(toSend) {
      case "send_question":
        const questionJSON = JSON.stringify({question_id: questionId, label: textLabel, boolean_list: selection})
        socket.emit('send_question', questionJSON);
        break;
      case "send_answer":
        const answerJSON = JSON.stringify({answer: answer})
          console.log(answer)
          console.log("answer sent")
        socket.emit('send_answer', answerJSON)
        break;
      case "send_guess":
        var index = 0;
        for(var i = 0; i < guessImage.length; i++) {
          if(guessImage[i]) {
            index = i;
            break;
          }
        }
        console.log(index)
        const guessJSON = JSON.stringify({guess: index})
        socket.emit('send_guess', guessJSON)
        break;
      default:
        break;
    }
  }

  useEffect(() => {
    var round;
    var countdown;
    if(timedState) {
      countdown = setTimeout(updateTimer, 10)
      round = setTimeout(roundDone, 1000)
    }
    socket.on('send_init_sets', data => {
      settimer(100);
      data = JSON.parse(data)
      setimages(data['images_set'])
      var selectionInit = []
      var guessImageInit = []
      for(var i = 0; i < data.images_set.length; i++) {
        selectionInit.push(false);
        guessImageInit.push(false);
      }
      setselection(selectionInit)
      setguessImage(guessImageInit)
      setoppimg(data.opponent_image)
      setquestions(data.questions_list)
      setloadingMessage("Waiting for server...")
    });
    socket.on('ask_question', function() {
      settimer(100);
      setgameState(3)
      settimedState(true)
      settoSend("send_question")
    });
    socket.on('wait', function() {
      settimer(100);
      setgameState(5)
      settimedState(true)
      settoSend("wait")
    });
    socket.on('answer_question', data => {
      settimer(100);
      data = JSON.parse(data)
      setoppQuestion(questions[data.question_id] + data.label)
      setgameState(4)
      settimedState(true)
      settoSend("send_answer")
    });
    socket.on('win', function() {
      console.log("Make win screen");
    });
    socket.on('lose', function() {
      console.log("Make loss screen");
    });
    return function cleanUp() {
      clearTimeout(countdown);
      clearTimeout(round);
    }
  }, [questions, updateTimer, roundDone, timedState]);

  function startGame() {
    console.log("start game")
    socket.emit('initialize_player')
    setgameState(3)
    settimedState(true)
  }

  function chooseImage(id) {
    var newGuessImage = []
    for(var i = 0; i < guessImage.length; i++) {
      newGuessImage.push(false);
    }
    if(guessImage[id] === true) {
      newGuessImage[id] = false;
    } else {
      newGuessImage[id] = true;
    }
    setguessImage(newGuessImage)
  }

  function selectImage(id) {
    const newSelection = []
    for(var i = 0; i < selection.length; i++) {
      if(selection[i] === true) {
        newSelection.push(true);
      } else {
        newSelection.push(false);
      }
    }
    if(newSelection[id] === true) {
      newSelection[id] = false;
    } else {
      newSelection[id] = true;
    }
    setselection(newSelection);
  }
  
  switch(gameState){
    case 1: 
    return (
      <div>
        <Header/>
        <Loading text={loadingMessage}/>
      </div>
    );
    case 2: 
      return (
        <div>
          <Header enabled="true" timer={timer}/>
          <Loading text="Opponents turn, please wait."/>
        </div>
      );
    case 3: 
      return (
        <div>
          <Header enabled="true" timer={timer}/>
          <QuestionsPage questions={questions} images={images} selection={selection} guessImage={guessImage} askButton={askQuestion} toGuess={() => toGuessPage(true)}/>
        </div>
      );
    case 4: 
      return (
        <div>
          <Header enabled="true" timer={timer}/>
          <AnswerPage source={oppimg} question={oppQuestion} answer={answerQuestion}/>
        </div>
      );
    case 5: 
      return (
        <div>
          <Header enabled="true" timer={timer}/>
          <EliminationPage images={images} selection={selection} guessImage={guessImage} onclick={selectImage}/>
        </div>
      );
    case 6: 
      return (
        <div>
          <Header enabled="true" timer={timer}/>
          <GuessPage images={images} selection={selection} guessImage={guessImage} onclick={chooseImage} toQuestion={() => toGuessPage(false)} guessTheImage={guessTheImage}/>
        </div>
      );
    case 0:
    default:
      return (
        <div>
          <Header />
          <Home startButton={startGame}/>
        </div>
      );
  }
}

export default App
