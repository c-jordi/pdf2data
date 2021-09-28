import {SimpleButton} from "../../../components/inputs";
import { BiImport } from "react-icons/bi";

const Header = () => {
    return   <div className="projects-header">
        <h2>Projects</h2>
        <SimpleButton> <BiImport/> Import</SimpleButton>
    </div>
}

export default Header;