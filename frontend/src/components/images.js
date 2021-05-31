import '../css/images.css'
import '../css/main.css';

const imageList = [
    {url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png',
    id: 0,
    selected: true}
]

const images = () => {
    var imgs = []
    for(var i = 0; i < 20; i++) {
        var extraClass = ""
        if(imageList[0].selected) {
            extraClass = "Selected"
        }
        imgs.push(<div className={"ImageContainer " + extraClass} style={{backgroundImage: 'url(' + imageList[0].url + ')'}}></div>)
    }
    return (
        <div className="Images Centering">
            {imgs}
        </div>
    )
}

export default images
