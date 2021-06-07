import '../css/answerPage.css'

const answerPage = (props) => {
    return (
        <div className="AnswerPage Centering">
            <div className="ImageOpponent" style={{backgroundImage: 'url(' + props.source + ')'}}></div>
            <h1>{props.question}</h1>
            <div className="Buttons">
                <button onClick={() => props.answer(0)} className="btn">No</button>
                <button onClick={() => props.answer(1)} className="btn">Probably no</button>
                <button onClick={() => props.answer(2)} className="btn">Probably yes</button>
                <button onClick={() => props.answer(3)} className="btn">Yes</button>
            </div>
        </div>
    )
}

export default answerPage
