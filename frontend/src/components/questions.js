import '../css/questions.css'
import '../css/main.css';

const questions = (props) => {
    var options = []
    for(var i = 0; i < props.questions.length; i++) {
        const x = i;
        options.push(<option value={x}>{props.questions[i]}</option>)
    }

    return (
        <div className="Questions Centering">
            <div>
                <select id="questionSelect">
                    {options}
                </select>
            </div>
            <div>
                <textarea id="areaText" rows="1"></textarea>
            </div>
            <div className="Buttons">
                <button onClick={() => props.askButton(document.getElementById("questionSelect").value, document.getElementById("areaText").value)} className="btn">Ask</button>
                <button onClick={props.toGuess} className="btn">Guess</button>
            </div>
        </div>
    )
}

export default questions
