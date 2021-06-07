import '../css/header.css';
import '../css/main.css';
import logo from '../resources/logo.png';

const header = (props) => {
    return (
        <div className="Header Centering">
            { props.enabled ? <div className="Timer">
                <div className="Timeleft" style={{width: props.timer+"%"}}></div>
            </div> : null }
            <img src={logo} className="Logo" alt="logo"/>
        </div>
    )
}

header.defaultProps = {
    enabled: false,
    time: 0,
}

export default header
