import '../css/loading.css';
import '../css/main.css';

const endPage = (props) => {
    return (
        <div className="Loading Centering">
            <div>
                <h1>{props.text}</h1>
            </div>
        </div>
    )
}

endPage.defaultProps = {
    text: 'The game has ended.',
}

export default endPage
