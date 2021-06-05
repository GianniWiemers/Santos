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

const App = (prosp) => {
  
  const [gameState, setgameState] = useState(6);
  const [timer, settimer] = useState(100);
  const [images, setimages] = useState(['https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png']);
  const [questions, setquestions] = useState([]);
  const [selection, setselection] = useState([true, true]);
  const [guessImage, setguessImage] = useState([false, false]);
  const [oppQuestion, setoppQuestion] = useState("no opponent question");
  const [oppimg, setoppimg] = useState('https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png');
  const [loadingMessage, setloadingMessage] = useState("Searching for another player...")
  const [timedState, settimedState] = useState(false);

  function updateTimer() {
    if(timer <= 0) {
      emitToSocket();
      setgameState(1);
      settimer(100);
      settimedState(false);
    } else {
      settimer(timer - 0.1)
    }
  }

  function emitToSocket() {
    switch(gameState) {
      case 3:
        const questionJSON = JSON.stringify({question_id: 0, label: "", boolean_list: selection})
        socket.emit('send_question', questionJSON);
        break;
      case 4:
        const answerJSON = JSON.stringify({answer: 0})
        socket.emit('send_answer', answerJSON)
        break;
      case 8:
        const guessJSON = JSON.stringify({guess: 0})
        socket.emit('send_guess', guessJSON)
        break;
      default:
        break;
    }
  }

  useEffect(() => {
    var countdown;
    if(timedState) {
      countdown = setTimeout(updateTimer, 10)
    }
    socket.on('send_init_sets', data => {
      setimages(data.images_set)
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
      setgameState(3)
    });
    socket.on('wait', function() {
      setgameState(5)
    });
    socket.on('answer_question', data => {
      setoppQuestion(questions[data.question_id] + data.label)
      setgameState(4)
    });
    socket.on('win', function() {
      console.log("Make win screen");
    });
    socket.on('lose', function() {
      console.log("Make loss screen");
    });
    return function cleanUp() {
      clearTimeout(countdown);
    }
  }, [questions, updateTimer, timedState]);

  function startGame() {
    socket.emit('initialize_player')
    setgameState(2)
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
          <QuestionsPage images={images} selection={selection} guessImage={guessImage}/>
        </div>
      );
      case 4: 
        return (
          <div>
            <Header enabled="true" timer={timer}/>
            <AnswerPage source={oppimg} question={oppQuestion}/>
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
              <GuessPage images={images} selection={selection} guessImage={guessImage} onclick={chooseImage}/>
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
