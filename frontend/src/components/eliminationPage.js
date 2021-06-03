import '../css/eliminationPage.css'
import '../css/main.css'
import Images from './images'

const eliminationPage = (props) => {
    return (
        <div className="ElimPage Centering">
            <div className="Answer Centering">
                <h1>Select the images that you wish to eliminate based on your opponents answers:</h1>
                <h2>{props.question}</h2>
                <h3>{props.answer}</h3>
            </div>
            <Images images={props.images} selection={props.selection} guessImage={props.guessImage} onclick={props.onclick}/>
        </div>
    )
}

export default eliminationPage
