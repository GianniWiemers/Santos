import Loading from './components/loading'
import Header from './components/header'
import Home from './components/home'
import QuestionsPage from './components/questionsPage'
import AnswerPage from './components/answerPage'
import EliminationPage from './components/eliminationPage'
import React from 'react';

class App extends React.Component {
  
  constructor() {
    super();
    this.state = {
      gameState: 5,
      date: new Date(),
      timer: 100
    };
  }

  setGameState = (state) => {
    clearInterval(this.round);
    clearInterval(this.timeLeft);
    switch(state) {
      case 1:
        this.setState({gameState: 1, date: new Date()});
        this.round = setInterval(
          () => this.setGameState(2),
          5000
        );
        break;
      case 2:
        this.setState({gameState: 2, date: new Date(), timer: 100});
        this.round = setInterval(
          () => this.setGameState(0),
          10000
        );
        this.timeLeft = setInterval(
          () => this.setState({timer: this.state.timer-0.1}),
          10
        );
        break;
      case 0:
      default:
        this.setState({gameState: 0});
        break;
    }
  }

  render() {
    switch(this.state.gameState){
      case 1: 
      return (
        <div>
          <Header/>
          <Loading text="Looking for a game..."/>
        </div>
      );
      case 2: 
        return (
          <div>
            <Header enabled="true" timer={this.state.timer}/>
            <Loading text="Opponents turn, please wait."/>
          </div>
        );
      case 3: 
        return (
          <div>
            <Header enabled="true" timer={this.state.timer}/>
            <QuestionsPage />
          </div>
        );
        case 4: 
          return (
            <div>
              <Header enabled="true" timer={this.state.timer}/>
              <AnswerPage />
            </div>
          );
        case 5: 
          return (
            <div>
              <Header enabled="true" timer={this.state.timer}/>
              <EliminationPage />
            </div>
          );
      case 0:
      default:
        return (
          <div>
            <Header />
            <Home startButton={() => this.setGameState(1)}/>
          </div>
        );
    }
  }
}

export default App;
