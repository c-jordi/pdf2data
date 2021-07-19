import "./style.scss";
import PropTypes from "prop-types";

const Section = ({ header, caption, children }) => {
	return (
		<div className="section">
			<div className="header">{header}</div>
			<div className="caption">{caption}</div>
			{children}
		</div>
	);
};

Section.propTypes = {
	header: PropTypes.string,
	caption: PropTypes.string,
};

Section.defaultProps = {
	header: "",
	caption: "",
};

export default Section;
