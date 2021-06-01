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
  
  const [gameState, setgameState] = useState(0);
  const [date, setdate] = useState(new Date());
  const [timer, settimer] = useState(100);
  const [images, setimages] = useState([]);
  const [selection, setselection] = useState([]);
  const [oppimg, setoppimg] = useState();
  const [loadingMessage, setloadingMessage] = useState("Searching for another player")

  useEffect(() => {
    socket.on('game_found', data => {
      setimages(data.imgs)
      setoppimg(data.oppImg)
      if(data.first === 0) {
        setgameState(2)
      } else {
        setgameState(3)
      }
    });
    socket.on('next_round', data => {
      setgameState(data.nextRound)
    });
  }, []);

  const setGameState = (state) => {
    switch(state) {
      case 1:
        setgameState(2)
        setdate(new Date())
        break;
      case 2:
        setgameState(2);
        settimer(100);
        setdate(new Date());
        const round = setInterval(
          () => setGameState(0),
          10000
        );
        const timeLeft = setInterval(
          () => settimer(timer-0.1),
          10
        );
        break;
      case 0:
      default:
        setgameState(0);
        break;
    }
  }

  const startGame = () => {
    socket.emit('initialize_player')
    setGameState(1)
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
          <QuestionsPage />
        </div>
      );
      case 4: 
        return (
          <div>
            <Header enabled="true" timer={timer}/>
            <AnswerPage />
          </div>
        );
      case 5: 
        return (
          <div>
            <Header enabled="true" timer={timer}/>
            <EliminationPage />
          </div>
        );
        case 6: 
          return (
            <div>
              <Header enabled="true" timer={timer}/>
              <GuessPage />
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
