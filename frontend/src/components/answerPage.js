import '../css/answerPage.css'

const answerPage = (props) => {
    return (
        <div className="AnswerPage Centering">
            <div className="ImageOpponent" style={{backgroundImage: 'url(' + props.image + ')'}}></div>
            <h1>{props.question} {props.word}?</h1>
            <div className="Buttons">
                <button className="btn">No</button>
                <button className="btn">Probably no</button>
                <button className="btn">Probably yes</button>
                <button className="btn">Yes</button>
            </div>
        </div>
    )
}

answerPage.defaultProps = {
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png',
    question: "Does the image contain",
    word: "a cat"
}

export default answerPage
