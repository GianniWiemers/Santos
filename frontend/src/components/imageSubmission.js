const imageSubmission = (props) => {
    return (
        <div className="Questions Centering">
            <h1>Please select the desired image</h1>
            <div className="ButtonContainer">
                <button onClick={props.toQuestion} className="btn">Back</button>
                <button onClick={props.guessImage} className="btn">Guess</button>
            </div>
        </div>
    )
}

export default imageSubmission
