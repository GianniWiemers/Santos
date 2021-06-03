import '../css/images.css'
import '../css/main.css';

const images = (props) => {

    var imgs = []
    for(var i = 0; i < props.images.length; i++) {
        var extraClass = ""
        if(!props.selection[i] && !props.guess) {
            extraClass = "Selected"
        } else if(props.guessImage[i] && props.guess) {
            extraClass = "Guess"
        }
        const index = i;
        imgs.push(<div onClick={() => props.onclick(index)} className={"ImageContainer " + extraClass} style={{backgroundImage: 'url(' + props.images[0] + ')'}}></div>)
    }
    return (
        <div className="Images Centering">
            {imgs}
        </div>
    )
}

images.defaultProps = {
    onclick: () => {},
    guess: false
}

export default images
