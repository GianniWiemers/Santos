import icon from '../resources/loading.png';
import '../css/loading.css';
import '../css/main.css';

const loading = (props) => {
    return (
        <div className="Loading centering">
            <div>
                <img src={icon} className="Loading-icon" alt="loading"/>
                <h1>{props.text}</h1>
            </div>
        </div>
    )
}

loading.defaultProps = {
    text: 'Loading, please wait.',
}

export default loading
