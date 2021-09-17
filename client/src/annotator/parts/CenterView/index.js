import "./style.scss"

const CenterView = (props) => {
    const coords = {
        position: "absolute",
        top: 44,
        left: 300,
        right: props.right,
        bottom : 0,
    }
    return <div className="centerview" style={coords}>Center</div>
}

export default CenterView;