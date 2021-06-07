import '../css/home.css';
import '../css/main.css';

const home = (props) => {
    return (
        <div className="Home Centering">
            <button className="btn" onClick={props.startButton}>Play!</button>
        </div>
    )
}

export default home
