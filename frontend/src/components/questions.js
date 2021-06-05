import '../css/questions.css'
import '../css/main.css';

const questions = () => {
    return (
        <div className="Questions Centering">
            <div>
                <select>
                    <option value="0">Does the image contain ...?</option>
                    <option value="1">Is the image related to ...?</option>
                    <option value="2">Can the image be used for ...?</option>
                </select>
            </div>
            <div>
                <textarea rows="1"></textarea>
            </div>
            <div className="Buttons">
                <button className="btn">Ask</button>
                <button className="btn">Guess</button>
            </div>
        </div>
    )
}

export default questions
