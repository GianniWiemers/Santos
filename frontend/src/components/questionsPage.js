import '../css/questionsPage.css'
import '../css/main.css'
import Questions from './questions'
import Images from './images'

const questionsPage = (props) => {
    return (
        <div className="QuestionsPage Centering">
            <Images images={props.images} selection={props.selection} guessImage={props.guessImage}/>
            <Questions askButton={props.askButton} toGuess={props.toGuess} questions={props.questions}/>
        </div>
    )
}

export default questionsPage
