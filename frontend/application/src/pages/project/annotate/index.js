import Toolbar from "./Toolbar.js"
import Window from "./Window.js"
import Leftbar from "./Leftbar.js"
import Rightbar from "./Rightbar.js"
import Mainview from "./Mainview.js"
import "./style.scss";

const Annotate = () => {
	return <div className="annotate">
		<Toolbar></Toolbar>
		<Window>
			<Leftbar></Leftbar>
			<Mainview></Mainview>
			<Rightbar></Rightbar>
		</Window>
		
	</div>
};	

export default Annotate;
