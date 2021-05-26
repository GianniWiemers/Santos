import '../css/images.css'
import '../css/main.css';

const imageList = [
    {url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/488px-No-Image-Placeholder.svg.png',
    id: 0}
]

const images = () => {
    var imgs = []
    for(var i = 0; i < 20; i++) {
        imgs.push(<div className="ImageContainer" style={{backgroundImage: 'url(' + imageList[0].url + ')'}}></div>)
    }
    return (
        <div className="Images Centering">
            {imgs}
        </div>
    )
}

export default images
