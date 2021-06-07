import Images from './images'
import ImageSubmission from './imageSubmission'

const guessPage = (props) => {
    return (
        <div className="QuestionsPage Centering">
            <Images images={props.images} selection={props.selection} guessImage={props.guessImage} onclick={props.onclick} guess={true}/>
            <ImageSubmission guessImage={props.guessTheImage} toQuestion={props.toQuestion}/>
        </div>
    )
}

export default guessPage
