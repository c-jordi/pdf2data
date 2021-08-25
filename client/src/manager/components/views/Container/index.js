import "./style.scss";

const Container = ({ children, id }) => {
	return <div className="container" id={id}>{children}</div>;
};

export default Container;
