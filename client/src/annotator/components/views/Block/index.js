import PropTypes from "prop-types";
import './style.scss'

const Block = ({title,children, flush}) => {

    const _className = "content" + (flush ? " flush" : "");

    return <div className="block">
        <div className="title">{title}</div>
        <div className={_className}>{children}</div>
    </div>
}

Block.defaultProps = {
    flush : false
}

export default Block;