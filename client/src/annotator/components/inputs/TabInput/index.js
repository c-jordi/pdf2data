import PropTypes from "prop-types";
import "./style.scss";


const TabInput = ({value, onChange, options}) => {

    const renderTab = (opt) => {

        const isActive = opt.value === value;
        const handleClick = () => {
            if (!isActive) onChange({type:"overwrite",value:opt.value});
        }
        const className = "d-tab-item" + (isActive? " active" : "");
        return <div className={className} key={opt.value} onClick={handleClick}>{opt.label}</div>
    }

    const renderTabs = (opts) => {
        return opts.map(renderTab)
    }

    return <div className='d-tab-input'>
        {renderTabs(options)}
    </div>
}

TabInput.propTypes = {
    value : PropTypes.string, //.isRequired,
    onChange : PropTypes.func.isRequired,
	options : PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.object,
        value : PropTypes.string
      }))
};

TabInput.defaultProps = {
    value : "random",
	options : [
        {label: 'Random', value: 'random'},
        {label: 'All', value: 'all'},
    ],
    onChange : (log) => {console.log(log)}
};



export default TabInput;