import '../css/answerPage.css'

const answerPage = (props) => {
    return (
        <div className="AnswerPage Centering">
            <div className="ImageOpponent" style={{backgroundImage: 'url(' + props.source + ')'}}></div>
            <h1>{props.question}</h1>
            <div className="Buttons">
                <button className="btn">No</button>
                <button className="btn">Probably no</button>
                <button className="btn">Probably yes</button>
                <button className="btn">Yes</button>
            </div>
        </div>
    )
}

export default answerPage
